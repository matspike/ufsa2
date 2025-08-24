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
    """Parse an IANA-style MIME CSV (expects columns like Name, Template).

    Creates concepts where label=Name and notation=Template (full media type).
    Tolerates different capitalizations.
    """
    if not specification_url.startswith("fixtures://"):
        raise FixtureURLRequiredError()
    fixture_rel = specification_url.replace("fixtures://", "")
    fixture_path = Path(fixtures_dir) / fixture_rel
    tracker.track_file(fixture_path)

    scheme = ConceptScheme(id=standard_id, label=name)

    with fixture_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row:
                continue
            keys = {k.lower(): (v or "") for k, v in row.items()}
            label = keys.get("name") or keys.get("label") or keys.get("type")
            notation = keys.get("template") or keys.get("mime") or keys.get("value")
            if not (label and notation):
                # Skip incomplete rows
                continue
            # Build a stable id from notation (replace disallowed characters)
            slug = notation.replace("/", "_").replace("+", "_")
            cid = f"{standard_id}:{slug}"
            c = Concept(id=cid, label=label, notes={"notation": notation})
            c.in_scheme = concept_scheme_uri
            scheme.concepts[c.id] = c

    return scheme
