from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_ERR_PYYAML_REQUIRED = "pyyaml is required for profile operations"
_ERR_PROFILE_MAPPING = "profile YAML must be a mapping"

# Allow environments without pyyaml; keep a typed reference for type checkers.
yaml: Any | None = None
try:
    import yaml as _yaml  # type: ignore[import]

    yaml = _yaml
except Exception:  # pragma: no cover
    yaml = None


@dataclass
class ProfileViolation:
    path: str
    message: str


def _load_profile(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise RuntimeError(_ERR_PYYAML_REQUIRED)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError(_ERR_PROFILE_MAPPING)
    return data


def _load_concepts_labels(concepts_csv: Path) -> list[str]:
    labels: list[str] = []
    if not concepts_csv.exists():
        return labels
    with concepts_csv.open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            lbl = (row.get("pref_label") or "").strip()
            if lbl:
                labels.append(lbl)
    return labels


def evaluate_profile(profile_path: Path, build_dir: Path) -> dict[str, Any]:
    """Evaluate a profile's simple constraints against build/concepts.csv.

    - Supports: cardinality: required for path names matching concept labels.
    - Returns a report with violations and a pass/fail flag.
    """
    prof = _load_profile(profile_path)
    constraints = prof.get("spec", {}).get("constraints", [])
    concepts_csv = build_dir / "concepts.csv"
    labels = set(_load_concepts_labels(concepts_csv))
    violations: list[ProfileViolation] = []

    for c in constraints:
        if not isinstance(c, dict):
            continue
        path = str(c.get("path", "")).strip()
        if not path:
            continue
        card = str(c.get("cardinality", "")).strip().lower()
        if card == "required" and path not in labels:
            violations.append(
                ProfileViolation(
                    path=path,
                    message=f"required path '{path}' not found in concepts.csv",
                )
            )

    return {
        "profile": str(profile_path),
        "build": str(build_dir),
        "violations": [vi.__dict__ for vi in violations],
        "ok": len(violations) == 0,
    }
