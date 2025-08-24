from __future__ import annotations

import csv
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
):
    if not specification_url.startswith("fixtures://"):
        raise FixtureURLRequiredError()
    fixture_rel = specification_url.replace("fixtures://", "")
    fixture_path = Path(fixtures_dir) / fixture_rel
    tracker.track_file(fixture_path)

    scheme = ConceptScheme(id=standard_id, label=name)

    with fixture_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # Expect either columns: Code, Name or name, code; be tolerant
        for row in reader:
            keys = {k.lower(): v for k, v in row.items()}
            code = keys.get("code") or keys.get("alpha2") or keys.get("country") or keys.get("type")
            name_val = keys.get("name") or keys.get("country_name") or keys.get("subtype")
            if not code:
                # skip malformed row
                continue
            c = Concept(
                id=f"{standard_id}:{code}",
                label=name_val or code,
                notes={"code": code},
            )
            c.in_scheme = concept_scheme_uri
            scheme.concepts[c.id] = c

    return scheme
