from __future__ import annotations

import csv
import json
from pathlib import Path


def emit_candidate_mappings(candidates: list[tuple[str, str, float]], out_dir: Path) -> list[str]:
    # JSON
    p_json = out_dir / "mappings.candidates.json"
    p_json.write_text(
        json.dumps(
            [{"source": a, "target": b, "score": score} for a, b, score in candidates],
            indent=2,
        )
    )
    # CSV
    p_csv = out_dir / "mappings.candidates.csv"
    with p_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source", "target", "score"])
        for a, b, score in candidates:
            w.writerow([a, b, score])
    return [str(p_json), str(p_csv)]
