"""Naive SQL DDL parser (fixture-backed).

Parses simple ``CREATE TABLE`` statements and foreign keys from a SQL file into
table and column concepts, with hierarchical and related relations.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from ufsa_v2.core_models import Concept, ConceptScheme
from ufsa_v2.utils.errors import FixtureURLRequiredError
from ufsa_v2.utils.tracker import Tracker


def _parse_sql_tables(sql_text: str) -> list[dict[str, Any]]:
    """Very small parser for simple CREATE TABLE blocks used in fixtures.

    Returns a list of {table: str, columns: list[{name: str, type: str}]}
    """
    tables: list[dict[str, Any]] = []
    # naive: split by CREATE TABLE ... (...);
    pattern = re.compile(
        r"CREATE\s+TABLE\s+(?P<name>[\w\.`\"]+)\s*\((?P<body>.*?)\);",
        re.IGNORECASE | re.DOTALL,
    )
    col_pat = re.compile(
        r"^\s*([`\"']?)(?P<col>[\w]+)\1\s+(?P<type>[\w\(\)\,\s]+)",
        re.IGNORECASE,
    )
    fk_pat = re.compile(
        r"FOREIGN\s+KEY\s*\(\s*([`\"']?)(?P<src>[\w]+)\1\s*\)\s*REFERENCES\s+([`\"']?)(?P<tgt_table>[\w]+)\3\s*\(\s*([`\"']?)(?P<tgt_col>[\w]+)\5\s*\)",
        re.IGNORECASE,
    )
    for m in pattern.finditer(sql_text):
        tname = m.group("name").strip().strip('"').strip("`")
        body = m.group("body")
        cols: list[dict[str, str]] = []
        fkeys: list[dict[str, str]] = []
        for line in body.splitlines():
            line = line.strip().rstrip(",")
            if not line:
                continue
            if line.upper().startswith("FOREIGN KEY"):
                fm = fk_pat.search(line)
                if fm:
                    fkeys.append({
                        "src": fm.group("src"),
                        "tgt_table": fm.group("tgt_table"),
                        "tgt_col": fm.group("tgt_col"),
                    })
                continue
            if line.upper().startswith("PRIMARY KEY"):
                continue
            cm = col_pat.match(line)
            if cm:
                cols.append({"name": cm.group("col"), "type": cm.group("type").strip()})
        tables.append({"table": tname, "columns": cols, "fkeys": fkeys})
    return tables


def parse(
    *,
    standard_id: str,
    name: str,
    governing_body: str,
    specification_url: str,
    concept_scheme_uri: str,
    fixtures_dir: str,
    tracker: Tracker,
):
    """Parse SQL DDL into a ``ConceptScheme`` of tables and columns."""
    if not specification_url.startswith("fixtures://"):
        raise FixtureURLRequiredError()
    fixture_rel = specification_url.replace("fixtures://", "")
    fixture_path = Path(fixtures_dir) / fixture_rel
    tracker.track_file(fixture_path)

    sql_text = fixture_path.read_text(encoding="utf-8")

    scheme = ConceptScheme(id=standard_id, label=name)
    tables = _parse_sql_tables(sql_text)
    for t in tables:
        t_id = f"{standard_id}:{t['table']}"
        t_con = Concept(id=t_id, label=t["table"], notes={"kind": "table"})
        t_con.in_scheme = concept_scheme_uri
        scheme.concepts[t_id] = t_con
        for col in t.get("columns", []) or []:
            c_id = f"{standard_id}:{t['table']}.{col['name']}"
            c_con = Concept(
                id=c_id,
                label=f"{t['table']}.{col['name']}",
                notes={"data_type": col.get("type", ""), "kind": "column"},
            )
            c_con.in_scheme = concept_scheme_uri
            # parent relation
            c_con.broader.append(t_id)
            t_con.narrower.append(c_id)
            scheme.concepts[c_id] = c_con
        # Emit relatedMatch for simple FKs: src_col related tgt_table.tgt_col
        for fk in t.get("fkeys", []) or []:
            src_col_id = f"{standard_id}:{t['table']}.{fk['src']}"
            tgt_col_id = f"{standard_id}:{fk['tgt_table']}.{fk['tgt_col']}"
            if src_col_id in scheme.concepts and tgt_col_id in scheme.concepts:
                src = scheme.concepts[src_col_id]
                # Use related_match if model supports; else append to related
                if hasattr(src, "related_match"):
                    src.related_match.append(tgt_col_id)
                else:
                    src.related.append(tgt_col_id)

    return scheme
