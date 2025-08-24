from __future__ import annotations

import json
from pathlib import Path

from ufsa_v2.parsers import parser_ast_sql, parser_cyclonedx
from ufsa_v2.utils.tracker import Tracker


def test_sql_ast_foreign_key_relation_on_fixture(tmp_path: Path):
    """Ensure FK from orders.user_id -> users.user_id is emitted as a relation."""
    fixtures = Path("data/fixtures")
    tracker = Tracker(tmp_path / "tracker.json")

    scheme = parser_ast_sql.parse(
        standard_id="internal_dw_schema",
        name="Internal Data Warehouse Schema",
        governing_body="Internal",
        specification_url="fixtures://dw_schema.sql",
        concept_scheme_uri="http://ufsa.org/v2/ast/internal_dw_schema",
        fixtures_dir=str(fixtures),
        tracker=tracker,
    )

    src = "internal_dw_schema:orders.user_id"
    tgt = "internal_dw_schema:users.user_id"
    assert src in scheme.concepts and tgt in scheme.concepts
    c_src = scheme.concepts[src]
    assert (tgt in c_src.related_match) or (tgt in c_src.related)


def test_sql_ast_backtick_identifiers_and_fk(tmp_path: Path):
    """Backtick/quote handling and FK detection for simple MySQL-style DDL."""
    ddl = (
        "CREATE TABLE `a` (\n"
        "  `id` INTEGER,\n"
        "  PRIMARY KEY (`id`)\n"
        ");\n\n"
        "CREATE TABLE `b` (\n"
        "  `a_id` INTEGER,\n"
        "  FOREIGN KEY (`a_id`) REFERENCES `a`(`id`)\n"
        ");\n"
    )
    fixtures_dir = tmp_path / "fixtures"
    fixtures_dir.mkdir(parents=True, exist_ok=True)
    sql_path = fixtures_dir / "quoted.sql"
    sql_path.write_text(ddl)

    tracker = Tracker(tmp_path / "tracker.json")
    scheme = parser_ast_sql.parse(
        standard_id="quoted_schema",
        name="Quoted Identifiers Schema",
        governing_body="Internal",
        specification_url="fixtures://quoted.sql",
        concept_scheme_uri="http://ufsa.org/v2/ast/quoted_schema",
        fixtures_dir=str(fixtures_dir),
        tracker=tracker,
    )

    # Backticks stripped in IDs
    assert "quoted_schema:a" in scheme.concepts
    assert "quoted_schema:b" in scheme.concepts
    # Column concepts exist
    assert "quoted_schema:a.id" in scheme.concepts
    assert "quoted_schema:b.a_id" in scheme.concepts
    # FK relation exists from b.a_id -> a.id
    src = scheme.concepts["quoted_schema:b.a_id"]
    tgt_id = "quoted_schema:a.id"
    assert (tgt_id in src.related_match) or (tgt_id in src.related)


def test_cyclonedx_enrichment_fields(tmp_path: Path):
    """CycloneDX parser captures licenses, hashes, and externalReferences in notes."""
    enriched = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "components": [
            {
                "name": "demo",
                "version": "1.0.0",
                "purl": "pkg:npm/demo@1.0.0",
                "description": "Demo component",
                "bom-ref": "pkg:npm/demo@1.0.0",
                "licenses": [
                    {"license": {"id": "MIT"}},
                    {"expression": "Apache-2.0 WITH LLVM-exception"},
                ],
                "hashes": [{"alg": "SHA-256", "content": "abc123"}],
                "externalReferences": [
                    {"type": "website", "url": "https://example.com/demo"},
                    {"type": "vcs", "url": "https://github.com/example/demo"},
                ],
            }
        ],
        "dependencies": [],
    }

    fixtures_dir = tmp_path / "fixtures"
    fixtures_dir.mkdir(parents=True, exist_ok=True)
    sbom_path = fixtures_dir / "sbom_enriched.json"
    sbom_path.write_text(json.dumps(enriched))

    tracker = Tracker(tmp_path / "tracker.json")
    scheme = parser_cyclonedx.parse(
        standard_id="cyclonedx_enriched",
        name="CycloneDX Enriched",
        governing_body="CycloneDX",
        specification_url="fixtures://sbom_enriched.json",
        concept_scheme_uri="http://ufsa.org/v2/sbom/cyclonedx_enriched",
        fixtures_dir=str(fixtures_dir),
        tracker=tracker,
    )

    # Single component concept with enrichment in notes
    assert len(scheme.concepts) == 1
    concept = next(iter(scheme.concepts.values()))
    notes = concept.notes
    assert notes.get("licenses") and "MIT" in notes["licenses"]
    assert notes.get("hashes") and notes["hashes"].startswith("SHA-256:")
    assert notes.get("externalReferences") and "https://example.com/demo" in notes["externalReferences"]
