from __future__ import annotations

import csv
from pathlib import Path

from ufsa_v2.core_models import ConceptScheme


def emit(scheme: ConceptScheme, out_dir: Path) -> Path:
    p = out_dir / f"{scheme.id}.concepts.csv"
    with p.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "label", "in_scheme", "notes_json"])
        for c in scheme.concepts.values():
            import json

            writer.writerow([
                c.id,
                c.label,
                c.in_scheme or "",
                json.dumps(c.notes, ensure_ascii=False),
            ])
    return p
