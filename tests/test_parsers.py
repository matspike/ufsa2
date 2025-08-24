from pathlib import Path

from ufsa_v2.engine import emit_outputs, unify_schemes
from ufsa_v2.parsers import (
    csv_parser,
    fields_csv_parser,
    iana_csv_parser,
    json_schema_parser,
    rdf_parser,
)
from ufsa_v2.utils import fetcher as _fetcher
from ufsa_v2.utils.fetcher import graphql_fetch
from ufsa_v2.utils.profiles import evaluate_profile
from ufsa_v2.utils.tracker import Tracker


def test_json_schema_parser(tmp_path: Path):
    fixtures = Path("data/fixtures")
    tracker = Tracker(tmp_path / "tracker.json")
    scheme = json_schema_parser.parse(
        standard_id="fhir_r4_patient",
        name="FHIR Patient",
        governing_body="HL7",
        specification_url="fixtures://fhir/patient.schema.json",
        concept_scheme_uri="http://ufsa.org/v2/standards/fhir_r4_patient",
        fixtures_dir=str(fixtures),
        tracker=tracker,
    )
    assert scheme.concepts, "JSON schema should produce concepts"


def test_json_schema_observation_parser(tmp_path: Path):
    fixtures = Path("data/fixtures")
    tracker = Tracker(tmp_path / "tracker.json")
    scheme = json_schema_parser.parse(
        standard_id="fhir_r4_observation",
        name="FHIR Observation",
        governing_body="HL7",
        specification_url="fixtures://fhir/observation.schema.json",
        concept_scheme_uri="http://ufsa.org/v2/standards/fhir_r4_observation",
        fixtures_dir=str(fixtures),
        tracker=tracker,
    )
    assert any(cid.endswith(":code") or cid.endswith(":status") for cid in scheme.concepts), (
        "Observation schema should include key fields"
    )
    # ValueSet hook present for Observation.code
    code_concepts = [c for cid, c in scheme.concepts.items() if cid.endswith(":code") or cid.endswith(":code.coding[]")]
    assert any(c.notes.get("valueset_hint") == "loinc" for c in code_concepts)


def test_fetcher_pin_verify(tmp_path: Path):
    url = "https://example.com/spec"
    cache_dir = tmp_path / ".cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    key = _fetcher._cache_key(url)
    path = cache_dir / f"{key}.html"
    path.write_text("<html><body>ok</body></html>")
    # pin returns key when cached
    pinned = _fetcher.pin(url, cache_dir)
    assert pinned == key
    # verify confirms the pin
    assert _fetcher.verify(url, cache_dir, key) is True


def test_csv_parser(tmp_path: Path):
    fixtures = Path("data/fixtures")
    tracker = Tracker(tmp_path / "tracker.json")
    scheme = csv_parser.parse(
        standard_id="iso_3166_1_a2",
        name="ISO 3166-1 A2",
        governing_body="ISO",
        specification_url="fixtures://iso/iso_3166_1_a2.csv",
        concept_scheme_uri="http://ufsa.org/v2/standards/iso_3166_1_a2",
        fixtures_dir=str(fixtures),
        tracker=tracker,
    )
    assert any(c.endswith(":US") for c in scheme.concepts), "Should include US concept"


def test_rdf_parser(tmp_path: Path):
    fixtures = Path("data/fixtures")
    tracker = Tracker(tmp_path / "tracker.json")
    scheme = rdf_parser.parse(
        standard_id="w3c_skos_core",
        name="SKOS Core",
        governing_body="W3C",
        specification_url="fixtures://w3c/skos_core_min.rdf",
        concept_scheme_uri="http://www.w3.org/2004/02/skos/core#",
        fixtures_dir=str(fixtures),
        tracker=tracker,
    )
    assert scheme.concepts, "RDF parser should produce at least one concept"


def test_iana_csv_parser(tmp_path: Path):
    fixtures = Path("data/fixtures")
    tracker = Tracker(tmp_path / "tracker.json")
    scheme = iana_csv_parser.parse(
        standard_id="iana_mime_application",
        name="IANA MIME Application",
        governing_body="IETF / IANA",
        specification_url="fixtures://iana/application.csv",
        concept_scheme_uri="http://ufsa.org/v2/standards/iana_mime_application",
        fixtures_dir=str(fixtures),
        tracker=tracker,
    )
    # Ensure application/json is present via notation
    assert any(c.notes.get("notation") == "application/json" for c in scheme.concepts.values())


def test_shopify_fields_parser(tmp_path: Path):
    fixtures = Path("data/fixtures")
    tracker = Tracker(tmp_path / "tracker.json")
    scheme = fields_csv_parser.parse(
        standard_id="shopify_admin_product",
        name="Shopify Product",
        governing_body="Shopify",
        specification_url="fixtures://shopify/product_fields.csv",
        concept_scheme_uri="http://ufsa.org/v2/standards/shopify_admin_product",
        fixtures_dir=str(fixtures),
        tracker=tracker,
    )
    assert any(c.label == "title" for c in scheme.concepts.values())


def test_openfigi_fields_parser(tmp_path: Path):
    fixtures = Path("data/fixtures")
    tracker = Tracker(tmp_path / "tracker.json")
    scheme = fields_csv_parser.parse(
        standard_id="openfigi_v3",
        name="OpenFIGI Mapping",
        governing_body="OMG / Bloomberg L.P.",
        specification_url="fixtures://openfigi/mapping_fields.csv",
        concept_scheme_uri="http://ufsa.org/v2/standards/openfigi_v3",
        fixtures_dir=str(fixtures),
        tracker=tracker,
    )
    assert any(c.label == "figi" for c in scheme.concepts.values())


def test_shopify_order_fields_parser(tmp_path: Path):
    fixtures = Path("data/fixtures")
    tracker = Tracker(tmp_path / "tracker.json")
    scheme = fields_csv_parser.parse(
        standard_id="shopify_admin_order",
        name="Shopify Order",
        governing_body="Shopify",
        specification_url="fixtures://shopify/order_fields.csv",
        concept_scheme_uri="http://ufsa.org/v2/standards/shopify_admin_order",
        fixtures_dir=str(fixtures),
        tracker=tracker,
    )
    assert any(c.label == "shippingAddress" for c in scheme.concepts.values())


def test_idmap_emitter_outputs(tmp_path: Path):
    # Use existing registry dir with sample YAMLs and a minimal scheme to trigger emit
    fixtures = Path("data/fixtures")
    tracker = Tracker(tmp_path / "tracker.json")
    # Parse one small scheme to satisfy emit_outputs requirements
    scheme = fields_csv_parser.parse(
        standard_id="openfigi_v3",
        name="OpenFIGI Mapping",
        governing_body="OMG / Bloomberg L.P.",
        specification_url="fixtures://openfigi/mapping_fields.csv",
        concept_scheme_uri="http://ufsa.org/v2/standards/openfigi_v3",
        fixtures_dir=str(fixtures),
        tracker=tracker,
    )
    out_dir = tmp_path / "build"
    out_dir.mkdir(parents=True, exist_ok=True)
    unified = unify_schemes([scheme])
    _ = emit_outputs(unified, out_dir, tracker)
    # idmap emitter should produce identifier_systems.csv and mappings.csv
    assert (out_dir / "identifier_systems.csv").exists()
    assert (out_dir / "mappings.csv").exists()


def test_profiles_evaluator_required_path(tmp_path: Path):
    # Create a minimal concepts.csv with selected labels
    build_dir = tmp_path / "build"
    build_dir.mkdir(parents=True, exist_ok=True)
    (build_dir / "concepts.csv").write_text(
        "concept_id,pref_label,definition,notation,scheme_uri\nx:Address,Address,,,\nx:City,City,,,\n"
    )
    # Profile requires postalCode -> should be violation
    prof = tmp_path / "postal.profile.yaml"
    prof.write_text(
        """
kind: Profile
apiVersion: ufsa.org/v2.0
metadata:
  name: TestPostal
  target: core:Address
spec:
  constraints:
    - path: postalCode
      cardinality: required
        """
    )

    result = evaluate_profile(prof, build_dir)
    assert result["ok"] is False
    assert any("postalCode" in v["message"] for v in result["violations"])


def test_graphql_fetch_offline_cache(tmp_path: Path):
    cache = tmp_path / ".cache"
    cache.mkdir(parents=True, exist_ok=True)
    url = "https://example.org/graphql"
    query = "{ shop { name } }"
    # No cache yet, offline should return None
    assert graphql_fetch(url, query, cache, offline=True) is None
    # Create a cached response to simulate prior fetch
    import hashlib

    key_src = f"{url}\n{query}".encode()
    key = hashlib.sha256(key_src).hexdigest()
    path = cache / f"{key}.json"
    path.write_text("{}")
    # Now offline should return the path
    got = graphql_fetch(url, query, cache, offline=True)
    assert got and got.exists()


def test_scraper_extract_table_rows(tmp_path: Path):
    from ufsa_v2.utils.scraper import extract_table_rows

    html = """
    <html><body>
    <table>
      <tr><th>Name</th><th>Price</th></tr>
      <tr><td>Widget</td><td>$10</td></tr>
    </table>
    </body></html>
    """
    p = tmp_path / "t.html"
    p.write_text(html)
    rows = extract_table_rows(p)
    assert rows and rows[0] == ["Name", "Price"] and rows[1] == ["Widget", "$10"]
