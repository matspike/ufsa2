"""Pipeline orchestration for UFSA v2.

This module wires together the pointer registry, parser modules, and emitters to
produce normalized artifacts. The runtime model is defined in
``ufsa_v2.core_models`` and is intentionally minimal. The primary entrypoint is
``run_pipeline`` which returns a list of output paths and updates a ``Tracker``.
"""

from __future__ import annotations

import importlib
import json
import logging
from pathlib import Path
from typing import Protocol, cast, runtime_checkable

import yaml  # type: ignore[import]
from jsonschema import validate as jsonschema_validate  # type: ignore[import]

from .core_models import (
    ConceptScheme,
    PipelineResult,
    Registry,
    UFSAStandard,
)
from .utils.tracker import Tracker


def load_registry(path: Path) -> Registry:
    """Load and optionally validate the pointer registry YAML.

    Args:
        path: Filesystem path to the registry YAML.

    Returns:
        Parsed ``Registry`` object containing standards to ingest.
    """
    data = yaml.safe_load(path.read_text())
    # Validate against schema if available
    schema_path = Path(__file__).parent / "registry" / "registry.schema.json"
    try:
        if schema_path.exists():
            import json as _json

            schema = _json.loads(schema_path.read_text())
            jsonschema_validate(instance=data, schema=schema)
    except Exception:
        logging.getLogger(__name__).debug(
            "Registry schema validation skipped due to error", exc_info=True
        )
    standards = [
        UFSAStandard(
            standard_id=entry["standard_id"],
            name=entry["name"],
            governing_body=entry["governing_body"],
            specification_url=entry["specification_url"],
            data_format=entry["data_format"],
            parser_module=entry["parser_module"],
            concept_scheme_uri=entry["concept_scheme_uri"],
        )
        for entry in data.get("standards", [])
    ]
    return Registry(standards=standards)


@runtime_checkable
class _ParserModule(Protocol):
    def parse(
        self,
        *,
        standard_id: str,
        name: str,
        governing_body: str,
        specification_url: str,
        concept_scheme_uri: str,
        fixtures_dir: str,
        tracker: Tracker,
    ) -> ConceptScheme: ...


def parse_standard(
    std: UFSAStandard, fixtures_dir: Path, tracker: Tracker
) -> ConceptScheme:
    """Import the declared parser module and parse a single standard.

    Args:
        std: Pointer registry entry.
        fixtures_dir: Directory where ``fixtures://`` URLs are resolved.
        tracker: Artifact tracker to record file dependencies.

    Returns:
        ConceptScheme parsed from the source specification.
    """
    # Resolve parser
    module_path = std.parser_module
    mod = importlib.import_module(module_path)
    parser = cast(_ParserModule, mod)
    # Prefer fixture file path for deterministic bootstrap
    scheme = parser.parse(
        standard_id=std.standard_id,
        name=std.name,
        governing_body=std.governing_body,
        specification_url=std.specification_url,
        concept_scheme_uri=std.concept_scheme_uri,
        fixtures_dir=str(fixtures_dir),
        tracker=tracker,
    )
    return scheme


def unify_schemes(schemes: list[ConceptScheme]) -> dict[str, ConceptScheme]:
    """Unify a list of schemes into a dict keyed by scheme id.

    This bootstrap keeps schemes separate; future iterations may merge or
    de-duplicate across inputs here.
    """
    # In this bootstrap, keep schemes separate by id; mappings can add cross-links later
    index: dict[str, ConceptScheme] = {sch.id: sch for sch in schemes}
    return index


def emit_outputs(
    schemes: dict[str, ConceptScheme], out_dir: Path, tracker: Tracker
) -> list[str]:
    """Emit per-scheme artifacts and global tables.

    Emits JSON/CSV per scheme, a consolidated JSON index, global tables
    (concepts, relations, schemes), identifier/mapping registries, and mapping
    candidate sets. All outputs are tracked.
    """
    outputs: list[str] = []
    outputs += _emit_per_scheme_artifacts(schemes, out_dir, tracker)
    outputs += _emit_indexes(schemes, out_dir, tracker)
    outputs += _emit_global_tables_and_registries(schemes, out_dir, tracker)
    return outputs


def _emit_per_scheme_artifacts(
    schemes: dict[str, ConceptScheme], out_dir: Path, tracker: Tracker
) -> list[str]:
    json_emitter = importlib.import_module("ufsa_v2.emitters.json_emitter")
    csv_emitter = importlib.import_module("ufsa_v2.emitters.csv_emitter")
    out: list[str] = []
    for scheme in schemes.values():
        p1 = json_emitter.emit(scheme, out_dir)
        p2 = csv_emitter.emit(scheme, out_dir)
        for p in (p1, p2):
            tracker.track_file(Path(p))
            out.append(str(p))
    return out


def _emit_indexes(
    schemes: dict[str, ConceptScheme], out_dir: Path, tracker: Tracker
) -> list[str]:
    out: list[str] = []
    # Write simple consolidated index
    index_path = out_dir / "concept_schemes.index.json"
    index_payload = {
        sch_id: {"label": sch.label, "concepts": list(sch.concepts.keys())}
        for sch_id, sch in schemes.items()
    }
    index_path.write_text(json.dumps(index_payload, indent=2))
    tracker.track_file(index_path)
    out.append(str(index_path))
    # Optional richer indexes
    try:
        index_emitter = importlib.import_module(
            "ufsa_v2.emitters.index_emitter"
        )
        if hasattr(index_emitter, "emit_global_indexes"):
            for gp in index_emitter.emit_global_indexes(schemes, out_dir):
                tracker.track_file(Path(gp))
                out.append(str(gp))
    except Exception:
        logging.getLogger(__name__).debug(
            "Global index emission skipped", exc_info=True
        )
    return out


def _emit_global_tables_and_registries(
    schemes: dict[str, ConceptScheme], out_dir: Path, tracker: Tracker
) -> list[str]:
    out: list[str] = []
    # Global tables
    try:
        tables_emitter = importlib.import_module(
            "ufsa_v2.emitters.tables_emitter"
        )
        if hasattr(tables_emitter, "emit_global_tables"):
            for gp in tables_emitter.emit_global_tables(schemes, out_dir):
                tracker.track_file(Path(gp))
                out.append(str(gp))
    except Exception:
        logging.getLogger(__name__).debug(
            "Global tables emission skipped", exc_info=True
        )
    # Identifier/mapping registries
    try:
        idmap_emitter = importlib.import_module(
            "ufsa_v2.emitters.idmap_emitter"
        )
        registry_dir = Path(__file__).parent / "registry"
        if hasattr(idmap_emitter, "emit_idmap_tables"):
            for gp in idmap_emitter.emit_idmap_tables(registry_dir, out_dir):
                tracker.track_file(Path(gp))
                out.append(str(gp))
    except Exception:
        logging.getLogger(__name__).debug(
            "Identifier/mapping emission skipped", exc_info=True
        )
    return out


def _generate_mapping_candidates(
    unified: dict[str, ConceptScheme],
) -> list[tuple[str, str, float]]:
    """Generate naive cross-scheme candidate mappings by label equality.

    Returns a list of (concept_id_a, concept_id_b, score) tuples.
    """
    # Build label -> concept ids per scheme
    by_label: dict[str, list[str]] = {}
    for sch in unified.values():
        for c in sch.concepts.values():
            key = c.label.strip().lower()
            by_label.setdefault(key, []).append(c.id)
    candidates: list[tuple[str, str, float]] = []
    for ids in by_label.values():
        if len(ids) > 1:
            for i in range(len(ids)):
                for j in range(i + 1, len(ids)):
                    candidates.append((ids[i], ids[j], 1.0))
    return candidates


def run_pipeline(
    registry_path: Path, out_dir: Path, tracker: Tracker
) -> PipelineResult:
    """Run the full UFSA pipeline.

    Steps:
      1) Load the pointer registry and parse each declared standard
      2) Unify schemes and emit per-scheme and global artifacts
      3) Generate naive mapping candidates

    Args:
        registry_path: Path to the pointer registry YAML.
        out_dir: Output directory for artifacts.
        tracker: Tracker instance to record file dependencies and meta.

    Returns:
        ``PipelineResult`` with emitted artifact paths.
    """
    registry = load_registry(registry_path)
    tracker.track_file(registry_path)

    # Fixtures alongside registry
    fixtures_dir = Path("data/fixtures").resolve()
    schemes: list[ConceptScheme] = []
    for std in registry.standards:
        scheme = parse_standard(std, fixtures_dir=fixtures_dir, tracker=tracker)
        schemes.append(scheme)

    unified = unify_schemes(schemes)
    # Enrich tracker meta with scheme labels and counts
    schemes_meta = tracker.meta.get("schemes")
    if not isinstance(schemes_meta, dict):
        schemes_meta = {}
    for sch_id, sch in unified.items():
        schemes_meta[str(sch_id)] = {
            "label": sch.label,
            "conceptCount": len(sch.concepts),
        }
    tracker.meta["schemes"] = schemes_meta
    # Track key project files for drift prevention
    for rel in ("pyproject.toml", "uv.lock", "README.md"):
        p = Path(rel)
        if p.exists():
            tracker.track_file(p)
    outputs = emit_outputs(unified, out_dir=out_dir, tracker=tracker)

    # Generate naive cross-scheme candidate mappings by label equality
    try:
        mapping_emitter = importlib.import_module(
            "ufsa_v2.emitters.mapping_emitter"
        )
        candidates = _generate_mapping_candidates(unified)
        for gp in mapping_emitter.emit_candidate_mappings(candidates, out_dir):
            tracker.track_file(Path(gp))
            outputs.append(str(gp))
        tracker.meta["mappingCandidates"] = len(candidates)
    except Exception:
        logging.getLogger(__name__).debug(
            "Mapping candidate generation skipped due to error", exc_info=True
        )
    return PipelineResult(outputs=outputs)
