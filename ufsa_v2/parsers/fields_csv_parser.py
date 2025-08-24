from __future__ import annotations

import csv
import re
from pathlib import Path

from ufsa_v2.core_models import Concept, ConceptScheme
from ufsa_v2.utils.errors import FixtureURLRequiredError
from ufsa_v2.utils.tracker import Tracker

_NON_ALNUM = re.compile(r"[^A-Za-z0-9_]+")


def _slugify(text: str) -> str:
    s = text.strip().replace(" ", "_")
    s = _NON_ALNUM.sub("_", s)
    return s.strip("_").lower() or "field"


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
    """Parse a generic field list CSV with columns like Name, Description.

    - Uses Name as label and generates a stable id from the name.
    - Stores description in notes.description when present.
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
            name_val = (row.get("Name") or row.get("name") or "").strip()
            desc_val = (row.get("Description") or row.get("description") or "").strip()
            if not name_val:
                continue
            slug = _slugify(name_val)
            cid = f"{standard_id}:{slug}"
            c = Concept(id=cid, label=name_val, notes={})
            if desc_val:
                c.notes["description"] = desc_val
            c.in_scheme = concept_scheme_uri
            scheme.concepts[c.id] = c

    # Post-processing for known relations (e.g., OpenFIGI composite/share class)
    if standard_id == "openfigi_v3":
        comp_id = f"{standard_id}:{_slugify('compositeFIGI')}"
        share_id = f"{standard_id}:{_slugify('shareClassFIGI')}"
        if comp_id in scheme.concepts and share_id in scheme.concepts:
            scheme.concepts[comp_id].narrower.append(share_id)
            scheme.concepts[share_id].broader.append(comp_id)

    return scheme
