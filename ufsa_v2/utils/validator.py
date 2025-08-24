from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml  # type: ignore[import]
from jsonschema import validate as jsonschema_validate  # type: ignore[import]


def _load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text())


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def validate_yaml_against_schema(yaml_path: Path, schema_path: Path) -> None:
    data = _load_yaml(yaml_path)
    schema = _load_json(schema_path)
    jsonschema_validate(instance=data, schema=schema)
