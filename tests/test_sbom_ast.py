from pathlib import Path

from ufsa_v2.engine import emit_outputs, unify_schemes
from ufsa_v2.parsers import parser_ast_sql, parser_cyclonedx
from ufsa_v2.utils.tracker import Tracker


def test_cyclonedx_fixture_parses_and_emits(tmp_path: Path):
    fixtures = Path("data/fixtures")
    tracker = Tracker(tmp_path / "tracker.json")
    scheme = parser_cyclonedx.parse(
        standard_id="cyclonedx_example",
        name="Example CycloneDX SBOM",
        governing_body="CycloneDX",
        specification_url="fixtures://sbom_example.json",
        concept_scheme_uri="http://ufsa.org/v2/sbom/cyclonedx_example",
        fixtures_dir=str(fixtures),
        tracker=tracker,
    )
    out_dir = tmp_path / "build"
    out_dir.mkdir(parents=True, exist_ok=True)
    unified = unify_schemes([scheme])
    outputs = emit_outputs(unified, out_dir, tracker)
    # Ensure software_components.csv was produced
    assert (out_dir / "software_components.csv").exists()
    # Ensure per-scheme CSV exists
    assert any(p.endswith("cyclonedx_example.concepts.csv") for p in outputs)


def test_sql_ast_fixture_parses_and_emits(tmp_path: Path):
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
    out_dir = tmp_path / "build"
    out_dir.mkdir(parents=True, exist_ok=True)
    unified = unify_schemes([scheme])
    outputs = emit_outputs(unified, out_dir, tracker)
    # Ensure database_schemas.csv was produced
    assert (out_dir / "database_schemas.csv").exists()
    # Ensure per-scheme CSV exists
    assert any(p.endswith("internal_dw_schema.concepts.csv") for p in outputs)
