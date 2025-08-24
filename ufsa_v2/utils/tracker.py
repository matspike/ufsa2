from __future__ import annotations

import hashlib
import json
import logging
import platform
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass
class Tracker:
    path: Path
    files: dict[str, dict[str, str]] = field(default_factory=dict)
    meta: dict[str, Any] = field(default_factory=dict)

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self._log = logging.getLogger(__name__)
        if self.path.exists():
            try:
                data = json.loads(self.path.read_text())
                self.files = data.get("files", {})
                self.meta = data.get("meta", {})
            except Exception:
                self._log.debug("Failed to read tracker file; starting fresh", exc_info=True)
                self.files = {}
                self.meta = {}
        else:
            self.files = {}
            self.meta = {}

    def track_file(self, path: Path) -> None:
        path = Path(path)
        rel = str(path)
        self.files[rel] = {
            "sha256": file_sha256(path),
        }

    def save(self) -> None:
        # Timestamp
        try:
            import datetime as _dt

            now = _dt.datetime.now(_dt.UTC)
            self.meta["generatedAt"] = now.isoformat()
        except Exception:
            logging.getLogger(__name__).debug("Failed to set generatedAt in tracker metadata", exc_info=True)

        # Environment basics
        self.meta["python"] = platform.python_version()

        # Git metadata (best-effort)
        try:
            import shutil
            import subprocess as _sp

            git = shutil.which("git")
            if not git:
                logging.getLogger(__name__).debug("git not found in PATH")
            else:
                head = _sp.run(  # noqa: S603 - git path resolved, args constant
                    [git, "rev-parse", "HEAD"],
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=2,
                ).stdout.strip()
                branch = _sp.run(  # noqa: S603 - git path resolved, args constant
                    [git, "rev-parse", "--abbrev-ref", "HEAD"],
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=2,
                ).stdout.strip()
                self.meta["git"] = {"commit": head, "branch": branch}
        except Exception:
            logging.getLogger(__name__).debug("Git metadata not available", exc_info=True)

        # Write JSON
        payload = {"meta": self.meta, "files": self.files}
        self.path.write_text(json.dumps(payload, indent=2))

        # Write human-friendly markdown
        try:
            md_path = Path("TRACKER.md")
            lines = ["# UFSA v2 Tracker\n", "\n"]
            lines.append("This file summarizes generated artifacts and their hashes to prevent drift.\n\n")
            lines.append("## Metadata\n\n")
            for k, v in sorted(self.meta.items()):
                lines.append(f"- {k}: {v}\n")
            lines.append("\n## Files\n\n")
            for rel, info in sorted(self.files.items()):
                lines.append(f"- {rel}  \n")
                lines.append(f"  - sha256: `{info.get('sha256', '')}`\n")
            md_path.write_text("".join(lines))
        except Exception:
            logging.getLogger(__name__).debug("Failed to write TRACKER.md", exc_info=True)


def compute_mismatches(tracker: Tracker) -> list[dict[str, str]]:
    """Compute mismatches between tracked file hashes and current filesystem.

    Returns a list of dicts with keys: path, expected_sha256, actual_sha256, exists
    """
    mismatches: list[dict[str, str]] = []
    for rel, info in tracker.files.items():
        p = Path(rel)
        expected = info.get("sha256", "")
        if not p.exists():
            mismatches.append({
                "path": rel,
                "expected_sha256": expected,
                "actual_sha256": "",
                "exists": "false",
            })
            continue
        actual = file_sha256(p)
        if actual != expected:
            mismatches.append({
                "path": rel,
                "expected_sha256": expected,
                "actual_sha256": actual,
                "exists": "true",
            })
    return mismatches


# ---------- Planning helpers (progress tracking) ----------

PlanTask = dict[str, Any]


def _ensure_plan(tracker: Tracker) -> dict[str, Any]:
    plan = tracker.meta.get("plan")
    if not isinstance(plan, dict):
        plan = {
            "tasks": [],
            "createdAt": tracker.meta.get("generatedAt", ""),
            "updatedAt": "",
        }
        tracker.meta["plan"] = plan
    if not isinstance(plan.get("tasks"), list):
        plan["tasks"] = []
    return plan


def _next_task_id(tasks: list[PlanTask]) -> int:
    max_id = 0
    for t in tasks:
        raw_id = t.get("id", 0)
        try:
            max_id = max(max_id, int(raw_id))
        except (TypeError, ValueError):
            logging.getLogger(__name__).debug("Non-integer task id encountered: %r", raw_id)
    return max_id + 1


def plan_add_task(tracker: Tracker, task: PlanTask) -> PlanTask:
    plan = _ensure_plan(tracker)
    tasks: list[PlanTask] = plan["tasks"]
    if "id" not in task:
        task["id"] = _next_task_id(tasks)
    # defaults
    task.setdefault("status", "todo")  # todo | in-progress | done | blocked
    task.setdefault("priority", "medium")  # low | medium | high
    task.setdefault("domain", "infrastructure")
    task.setdefault("category", "feature")
    tasks.append(task)
    plan["updatedAt"] = tracker.meta.get("generatedAt", "")
    return task


def plan_mark_task(tracker: Tracker, task_id: int, status: str) -> bool:
    plan = _ensure_plan(tracker)
    for t in plan["tasks"]:
        if int(t.get("id", -1)) == int(task_id):
            t["status"] = status
            plan["updatedAt"] = tracker.meta.get("generatedAt", "")
            return True
    return False


def plan_list(tracker: Tracker, status: str | None = None) -> list[PlanTask]:
    plan = _ensure_plan(tracker)
    tasks: list[PlanTask] = plan["tasks"]
    if status:
        return [t for t in tasks if t.get("status") == status]
    return tasks


def plan_stats(tracker: Tracker) -> dict[str, Any]:
    tasks = plan_list(tracker)
    total = len(tasks)
    by_status: dict[str, int] = {}
    for t in tasks:
        s = str(t.get("status", "todo"))
        by_status[s] = by_status.get(s, 0) + 1
    done = by_status.get("done", 0)
    progress = (done / total) * 100 if total else 0.0
    return {
        "total": total,
        "by_status": by_status,
        "progress_percent": round(progress, 1),
    }


def plan_seed_from_docs(tracker: Tracker) -> list[PlanTask]:
    """Seed a baseline plan derived from Docs 1 (coverage) and Doc 2 (core pattern).

    Idempotent: avoids duplicating tasks with the same title.
    """
    plan = _ensure_plan(tracker)
    existing_titles = {str(t.get("title", "")) for t in plan["tasks"]}
    seeds: list[PlanTask] = []

    def add(
        title: str,
        domain: str,
        category: str,
        priority: str,
        rationale: str,
        doc_ref: str,
    ) -> None:
        if title in existing_titles:
            return
        seeds.append({
            "title": title,
            "domain": domain,
            "category": category,
            "priority": priority,
            "status": "todo",
            "rationale": rationale,
            "doc_ref": doc_ref,
        })

    # Core pattern (Doc 2): metamodel and global tables completeness
    add(
        "Tighten SKOS mapping predicates and relations in model and outputs",
        "infrastructure",
        "model",
        "high",
        "Doc 2 emphasizes SKOS as the core; ensure predicates (exact/close/broad/narrow) supported in emitters",
        "Doc 2, Section II",
    )

    # Healthcare (FHIR)
    add(
        "FHIR: Add Encounter, Condition, Medication, Procedure (JSON Schema fixtures)",
        "healthcare",
        "coverage",
        "high",
        "Doc 1 Section 3.1 calls out breadth across resources",
        "Doc 1, 3.1",
    )
    add(
        "FHIR: Deepen Observation semantics (ValueSet hooks for Observation.code)",
        "healthcare",
        "depth",
        "high",
        "Doc 1 mentions coded value sets; prepare hooks for future LOINC integration",
        "Doc 1, 3.1",
    )

    # E-commerce (Shopify)
    add(
        "Shopify: Add Customer, InventoryItem, Fulfillment objects (fixtures)",
        "ecommerce",
        "coverage",
        "medium",
        "Extend beyond Product/Order for realistic domain coverage",
        "Doc 1, 3.2",
    )
    add(
        "Shopify: Implement basic HTML/GraphQL scraping fetcher with cache",
        "ecommerce",
        "depth",
        "high",
        "Doc 1 requires scraping for real sources; add fetcher layer with caching",
        "Doc 1, 3.2",
    )

    # Finance (OpenFIGI)
    add(
        "OpenFIGI: Model compositeFIGI/shareClassFIGI hierarchy and relations",
        "finance",
        "depth",
        "high",
        "Capture intended hierarchy and relations per Doc 1",
        "Doc 1, 3.3",
    )
    add(
        "Finance: Add ISIN and CUSIP fixtures and establish relatedMatch links to FIGI",
        "finance",
        "coverage",
        "medium",
        "Demonstrate cross-standard identifier mapping",
        "Doc 1, 3.3",
    )

    # Foundational
    add(
        "ISO: Add ISO 4217 currency and ISO 3166-2 subdivisions (fixtures)",
        "foundational",
        "coverage",
        "medium",
        "Broaden foundational standards for mappings",
        "Doc 1, 3.4",
    )
    add(
        "IANA: Cover text/*, image/*, audio/*, video/* in addition to application/*",
        "foundational",
        "coverage",
        "low",
        "Extend MIME type space for better mappings",
        "Doc 1, 3.4",
    )
    add(
        "SKOS: Full vocabulary ingestion instead of minimal subset",
        "foundational",
        "depth",
        "low",
        "Ensure complete vocabulary for richer relations",
        "Doc 1, 3.4",
    )

    # Infrastructure/platform
    add(
        "Fetcher: Add network fetchers with caching and hash pinning (offline by default)",
        "infrastructure",
        "platform",
        "high",
        "Enable real spec ingestion while preserving determinism",
        "Doc 1, Section I/III",
    )
    add(
        "Profiles: Support contextual overlays and mapping semantics in config",
        "infrastructure",
        "platform",
        "medium",
        "Prepare for domain-specific overlays and mapping preferences",
        "Doc 1, Section I",
    )
    add(
        "CI: Add CI to run check + pipeline; publish artifacts",
        "infrastructure",
        "ops",
        "medium",
        "Automate quality gates and artifact publication",
        "Doc 1, Section IV/V",
    )

    created: list[PlanTask] = []
    for s in seeds:
        created.append(plan_add_task(tracker, s))
    return created


def plan_seed_from_sbom_ast(tracker: Tracker) -> list[PlanTask]:
    """Seed tasks specifically for the SBOM/AST integration (Doc 4)."""
    plan = _ensure_plan(tracker)
    existing_titles = {str(t.get("title", "")) for t in plan["tasks"]}
    seeds: list[PlanTask] = []

    def add(
        title: str,
        domain: str,
        category: str,
        priority: str,
        status: str,
        rationale: str,
    ) -> None:
        if title in existing_titles:
            return
        seeds.append({
            "title": title,
            "domain": domain,
            "category": category,
            "priority": priority,
            "status": status,
            "rationale": rationale,
            "doc_ref": "docs/4_UFSA2.1_SBOM_AST.md",
        })

    add(
        "Phase 1: Create parser stubs (CycloneDX + SQL DDL)",
        "infrastructure",
        "feature",
        "high",
        "done",
        "Added parser_cyclonedx.py and parser_ast_sql.py with minimal fixture parsing",
    )
    add(
        "Phase 1: Pointer registry entries and fixtures (SBOM/AST)",
        "infrastructure",
        "config",
        "high",
        "done",
        "Appended cyclonedx_example and internal_dw_schema to pointer registry; added fixtures",
    )
    add(
        "Phase 2: Implement CycloneDX SBOM parser",
        "infrastructure",
        "feature",
        "medium",
        "in-progress",
        "Minimal transform from components/dependencies into SKOS; iterate if needed",
    )
    add(
        "Phase 2: Implement SQL DDL AST parser",
        "infrastructure",
        "feature",
        "medium",
        "in-progress",
        "Naive DDL parsing for tables/columns; future: sqlglot for robustness",
    )
    add(
        "Phase 3: Specialized emitters (software_components.csv, database_schemas.csv)",
        "infrastructure",
        "emitter",
        "medium",
        "done",
        "Emit specialized tables and exclude from generic concepts.csv",
    )
    add(
        "Phase 4: Tracker integration (track specialized outputs)",
        "infrastructure",
        "ops",
        "low",
        "done",
        "Outputs are automatically tracked via engine emit step",
    )
    add(
        "Phase 4: Sealing & packaging include new parser modules",
        "infrastructure",
        "automation",
        "low",
        "done",
        "SEAL scans ufsa_v2/; whitelist already captures sealed outputs",
    )

    created: list[PlanTask] = []
    for s in seeds:
        created.append(plan_add_task(tracker, s))
    return created


def plan_seed_from_state(tracker: Tracker) -> list[PlanTask]:
    """Seed tasks representing current achievements and plumbing based on tracker state."""
    plan = _ensure_plan(tracker)
    existing_titles = {str(t.get("title", "")) for t in plan["tasks"]}
    created: list[PlanTask] = []

    # Per-scheme integrations
    schemes = tracker.meta.get("schemes", {})
    if isinstance(schemes, dict):
        for sch_id, meta in schemes.items():
            title = f"Integrate {sch_id} — {meta.get('label', '')}"
            if title in existing_titles:
                continue
            domain = (
                "healthcare"
                if str(sch_id).startswith("fhir_")
                else (
                    "ecommerce"
                    if str(sch_id).startswith("shopify_")
                    else ("finance" if str(sch_id).startswith("openfigi_") else "foundational")
                )
            )
            created.append(
                plan_add_task(
                    tracker,
                    {
                        "title": title,
                        "domain": domain,
                        "category": "coverage",
                        "priority": "medium",
                        "status": "done",
                        "rationale": "Integrated via fixtures and parsers",
                        "doc_ref": "Docs 1 & 2",
                    },
                )
            )

    # Outputs plumbing
    files = tracker.files

    def _tracked(p: str) -> bool:
        return p in files

    if (
        _tracked("build/concept_schemes.csv")
        and _tracked("build/concepts.csv")
        and _tracked("build/semantic_relations.csv")
        and "Emit global tables" not in existing_titles
    ):
        created.append(
            plan_add_task(
                tracker,
                {
                    "title": "Emit global tables",
                    "domain": "infrastructure",
                    "category": "emitter",
                    "priority": "high",
                    "status": "done",
                    "rationale": "Global CSV tables are present in build/",
                    "doc_ref": "Doc 2, outputs",
                },
            )
        )
    if (
        _tracked("build/concept_schemes.index.json")
        and _tracked("build/concepts.all.json")
        and "Emit consolidated indexes" not in existing_titles
    ):
        created.append(
            plan_add_task(
                tracker,
                {
                    "title": "Emit consolidated indexes",
                    "domain": "infrastructure",
                    "category": "emitter",
                    "priority": "medium",
                    "status": "done",
                    "rationale": "Index and aggregates present in build/",
                    "doc_ref": "Doc 2, outputs",
                },
            )
        )
    if (
        tracker.meta.get("mappingCandidates", 0)
        and _tracked("build/mappings.candidates.json")
        and "Generate mapping candidates" not in existing_titles
    ):
        created.append(
            plan_add_task(
                tracker,
                {
                    "title": "Generate mapping candidates",
                    "domain": "infrastructure",
                    "category": "mapping",
                    "priority": "medium",
                    "status": "done",
                    "rationale": "Naive label-equality candidates generated",
                    "doc_ref": "Doc 2, mapping",
                },
            )
        )

    # Developer ergonomics present
    if Path("Makefile").exists() and "Makefile targets and uv scripts" not in existing_titles:
        created.append(
            plan_add_task(
                tracker,
                {
                    "title": "Makefile targets and uv scripts",
                    "domain": "infrastructure",
                    "category": "ops",
                    "priority": "low",
                    "status": "done",
                    "rationale": "Makefile present; uv scripts configured in pyproject",
                    "doc_ref": "Ops",
                },
            )
        )
    return created
