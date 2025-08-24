from __future__ import annotations

import csv
import json
from pathlib import Path

from ufsa_v2.core_models import ConceptScheme


def emit_global_indexes(schemes: dict[str, ConceptScheme], out_dir: Path) -> list[str]:
    out_paths: list[str] = []

    # Flat JSON list of all concepts
    all_concepts = []
    for sch_id, sch in schemes.items():
        for c in sch.concepts.values():
            all_concepts.append({
                "scheme": sch_id,
                "scheme_label": sch.label,
                "id": c.id,
                "label": c.label,
                "in_scheme": c.in_scheme,
                "notes": c.notes,
            })
    p_json = out_dir / "concepts.all.json"
    p_json.write_text(json.dumps(all_concepts, indent=2))
    out_paths.append(str(p_json))

    # Flat CSV list of all concepts
    p_csv = out_dir / "concepts.all.csv"
    with p_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["scheme", "scheme_label", "id", "label", "in_scheme", "notes_json"])
        for row in all_concepts:
            w.writerow([
                row["scheme"],
                row["scheme_label"],
                row["id"],
                row["label"],
                row["in_scheme"] or "",
                json.dumps(row["notes"], ensure_ascii=False),
            ])
    out_paths.append(str(p_csv))

    return out_paths
