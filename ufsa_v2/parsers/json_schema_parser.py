from __future__ import annotations

import json
from pathlib import Path

from ufsa_v2.core_models import Concept, ConceptScheme
from ufsa_v2.utils.errors import FixtureURLRequiredError
from ufsa_v2.utils.tracker import Tracker


def parse(
    *,
    standard_id: str,
    name: str,
    governing_body: str,
    specification_url: str,
    concept_scheme_uri: str,
    fixtures_dir: str,
    tracker: Tracker,
) -> ConceptScheme:
    # Resolve fixture path
    if not specification_url.startswith("fixtures://"):
        raise FixtureURLRequiredError()
    fixture_rel = specification_url.replace("fixtures://", "")
    fixture_path = Path(fixtures_dir) / fixture_rel
    text = fixture_path.read_text()
    tracker.track_file(fixture_path)
    data = json.loads(text)

    scheme = ConceptScheme(id=standard_id, label=name)

    def add_prop(path: str, schema: dict):
        label = schema.get("title") or path.split(".")[-1]
        c = Concept(id=f"{standard_id}:{path}", label=str(label), notes={})
        c.in_scheme = concept_scheme_uri
        if "type" in schema:
            c.notes["type"] = json.dumps(schema["type"]) if not isinstance(schema["type"], str) else schema["type"]
        if "description" in schema:
            c.notes["description"] = schema["description"]

        # FHIR Observation ValueSet hook for Observation.code
        if standard_id == "fhir_r4_observation" and (path == "code" or path == "code.coding[]"):
            # Hint that this property is typically bound to LOINC
            c.notes["valueset_hint"] = "loinc"

        scheme.concepts[c.id] = c

        # Recurse into nested properties
        props = schema.get("properties", {})
        for k, v in props.items():
            add_prop(f"{path}.{k}" if path else k, v)

        # Items for arrays
        items = schema.get("items")
        if isinstance(items, dict):
            add_prop(f"{path}[]", items)

    add_prop("", data)
    return scheme
