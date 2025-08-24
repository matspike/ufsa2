from __future__ import annotations

import json
from pathlib import Path

from ufsa_v2.core_models import ConceptScheme


def emit(scheme: ConceptScheme, out_dir: Path) -> Path:
    payload = {
        "id": scheme.id,
        "label": scheme.label,
        "concepts": [
            {
                "id": c.id,
                "label": c.label,
                "notes": c.notes,
                "in_scheme": c.in_scheme,
                "exact_match": getattr(c, "exact_match", []),
                "close_match": getattr(c, "close_match", []),
                "broad_match": getattr(c, "broad_match", []),
                "narrow_match": getattr(c, "narrow_match", []),
                "related_match": getattr(c, "related_match", []),
            }
            for c in scheme.concepts.values()
        ],
    }
    p = out_dir / f"{scheme.id}.concepts.json"
    p.write_text(json.dumps(payload, indent=2))
    return p
