from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import yaml  # type: ignore[import]


def _load_yaml(path: Path) -> Any:
    data = yaml.safe_load(path.read_text())
    return data


def emit_identifier_systems(registry_dir: Path, out_dir: Path) -> str | None:
    """Emit identifier systems catalog to CSV if registry exists.

    Expected YAML shape (minimal):
    systems:
      - id: iso-3166-1-a2
        name: ISO 3166-1 Alpha-2 Country Codes
        authority: ISO
        uri: https://www.iso.org/iso-3166-country-codes.html
        description: Two-letter country code set
    """
    src = registry_dir / "identifier_systems.yaml"
    if not src.exists():
        return None
    payload = _load_yaml(src)
    systems = payload.get("systems", []) if isinstance(payload, dict) else []
    out_path = out_dir / "identifier_systems.csv"
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "name", "authority", "uri", "description"])
        for s in systems:
            w.writerow([
                str(s.get("id", "")),
                str(s.get("name", "")),
                str(s.get("authority", "")),
                str(s.get("uri", "")),
                str(s.get("description", "")),
            ])
    return str(out_path)


def emit_mappings(registry_dir: Path, out_dir: Path) -> str | None:
    """Emit mappings CSV if registry exists.

    Expected YAML shape (minimal):
    mappings:
      - subject: urn:ufsa:id:openfigi
        predicate: skos:relatedMatch
        object: urn:ufsa:id:isin
        confidence: 0.6
        provenance: Doc 3 example
    """
    src = registry_dir / "mappings.yaml"
    if not src.exists():
        return None
    payload = _load_yaml(src)
    mappings = payload.get("mappings", []) if isinstance(payload, dict) else []
    out_path = out_dir / "mappings.csv"
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["subject", "predicate", "object", "confidence", "provenance"])
        for m in mappings:
            w.writerow([
                str(m.get("subject", "")),
                str(m.get("predicate", "")),
                str(m.get("object", "")),
                json.dumps(float(m.get("confidence", 1.0))),
                str(m.get("provenance", "")),
            ])
    return str(out_path)


def emit_idmap_tables(registry_dir: Path, out_dir: Path) -> list[str]:
    out: list[str] = []
    p1 = emit_identifier_systems(registry_dir, out_dir)
    if p1:
        out.append(p1)
    p2 = emit_mappings(registry_dir, out_dir)
    if p2:
        out.append(p2)
    return out
