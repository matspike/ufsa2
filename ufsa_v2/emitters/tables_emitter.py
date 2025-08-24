"""Emit consolidated CSV tables for schemes, concepts, relations, and specials.

This module writes the global tables described in the docs:
    - concept_schemes.csv
    - concepts.csv
    - semantic_relations.csv
    - software_components.csv (if present)
    - database_schemas.csv (if present)
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from ufsa_v2.core_models import Concept, ConceptScheme


def _write_concept_schemes_csv(
    schemes: dict[str, ConceptScheme], out_path: Path
) -> None:
    """Write ``concept_schemes.csv`` with id, label, URI, governing_body."""
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            ["scheme_id", "scheme_label", "scheme_uri", "governing_body"]
        )  # governing_body not tracked yet
        for sch_id, sch in sorted(schemes.items()):
            # Derive scheme_uri from first concept.in_scheme when available
            scheme_uri = ""
            for c in sch.concepts.values():
                if c.in_scheme:
                    scheme_uri = c.in_scheme
                    break
            w.writerow(
                [sch_id, sch.label, scheme_uri, ""]
            )  # governing_body placeholder


def _write_concepts_csv(
    schemes: dict[str, ConceptScheme], out_path: Path
) -> None:
    """Write ``concepts.csv`` excluding specialized kinds (software, db)."""
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            ["concept_id", "pref_label", "definition", "notation", "scheme_uri"]
        )  # aligns to docs
        for sch in schemes.values():
            for c in sch.concepts.values():
                # Exclude specialized concepts that will be emitted into dedicated tables
                kind = c.notes.get("kind", "")
                if kind in {"software_component", "table", "column"}:
                    continue
                definition = c.notes.get("description", "")
                notation = c.notes.get("notation", c.notes.get("code", ""))
                w.writerow(
                    [c.id, c.label, definition, notation, c.in_scheme or ""]
                )


def _write_semantic_relations_csv(
    schemes: dict[str, ConceptScheme], out_path: Path
) -> None:
    """Write ``semantic_relations.csv`` listing SKOS-style triples."""
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            ["subject_id", "predicate", "object_id"]
        )  # SKOS-style predicates as strings
        for sch in schemes.values():
            for c in sch.concepts.values():
                _write_relations_for_concept(w, c)


def _write_relations_for_concept(w: Any, c: Any) -> None:
    """Helper to write all relations for a single concept to the CSV writer."""
    for b in c.broader:
        w.writerow([c.id, "skos:broader", b])
    for n in c.narrower:
        w.writerow([c.id, "skos:narrower", n])
    for r in c.related:
        w.writerow([c.id, "skos:related", r])
    for x in getattr(c, "exact_match", []) or []:
        w.writerow([c.id, "skos:exactMatch", x])
    for x in getattr(c, "close_match", []) or []:
        w.writerow([c.id, "skos:closeMatch", x])
    for x in getattr(c, "broad_match", []) or []:
        w.writerow([c.id, "skos:broadMatch", x])
    for x in getattr(c, "narrow_match", []) or []:
        w.writerow([c.id, "skos:narrowMatch", x])
    for x in getattr(c, "related_match", []) or []:
        w.writerow([c.id, "skos:relatedMatch", x])


def emit_global_tables(
    schemes: dict[str, ConceptScheme], out_dir: Path
) -> list[str]:
    """Emit all global and specialized tables; return list of written paths."""
    out_paths: list[str] = []

    # concept_schemes.csv
    p_schemes = out_dir / "concept_schemes.csv"
    _write_concept_schemes_csv(schemes, p_schemes)
    out_paths.append(str(p_schemes))

    # concepts.csv
    p_concepts = out_dir / "concepts.csv"
    _write_concepts_csv(schemes, p_concepts)
    out_paths.append(str(p_concepts))

    # semantic_relations.csv
    p_rel = out_dir / "semantic_relations.csv"
    _write_semantic_relations_csv(schemes, p_rel)
    out_paths.append(str(p_rel))

    # Specialized outputs
    sw_path = _write_software_components(schemes, out_dir)
    if sw_path:
        out_paths.append(str(sw_path))

    db_path = _write_database_schemas(schemes, out_dir)
    if db_path:
        out_paths.append(str(db_path))

    return out_paths


def _write_software_components(
    schemes: dict[str, ConceptScheme], out_dir: Path
) -> Path | None:
    comps: list[Concept] = []
    for sch in schemes.values():
        for c in sch.concepts.values():
            if c.notes.get("kind") == "software_component":
                comps.append(c)
    if not comps:
        return None
    p_sw = out_dir / "software_components.csv"
    with p_sw.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            ["purl", "name", "version", "description", "scheme_uri"]
        )  # per doc
        for c in comps:
            purl = c.notes.get("purl", "")
            name = c.label
            version = c.notes.get("notation", "")
            desc = c.notes.get("description", "")
            w.writerow([purl, name, version, desc, c.in_scheme or ""])
    return p_sw


def _write_database_schemas(
    schemes: dict[str, ConceptScheme], out_dir: Path
) -> Path | None:
    tables_cols: list[Concept] = []
    for sch in schemes.values():
        for c in sch.concepts.values():
            if c.notes.get("kind") in {"table", "column"}:
                tables_cols.append(c)
    if not tables_cols:
        return None
    p_db = out_dir / "database_schemas.csv"
    with p_db.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            ["table_name", "column_name", "data_type", "concept_uri"]
        )  # per doc
        # Emit tables as rows with column_name empty; columns with both
        for c in tables_cols:
            if c.notes.get("kind") == "table":
                w.writerow([c.label, "", "", c.id])
            else:
                # column: label is table.col
                table_name, _, col_name = c.label.partition(".")
                w.writerow(
                    [
                        table_name,
                        col_name,
                        c.notes.get("data_type", ""),
                        c.id,
                    ]
                )
    return p_db
