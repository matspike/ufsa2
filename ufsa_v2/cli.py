"""Command-line interface for UFSA v2.

Provides subcommands to run the pipeline, inspect the tracker, manage the plan,
validate registries and profiles, and use the offline-first fetcher utilities.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import run_pipeline
from .utils.fetcher import (
    fetch,
    graphql_fetch,
)
from .utils.fetcher import (
    pin as fetch_pin,
)
from .utils.fetcher import (
    verify as fetch_verify,
)
from .utils.profiles import evaluate_profile
from .utils.scraper import extract_table_rows
from .utils.tracker import (
    Tracker,
    compute_mismatches,
    plan_add_task,
    plan_list,
    plan_mark_task,
    plan_seed_from_docs,
    plan_seed_from_sbom_ast,
    plan_seed_from_state,
    plan_stats,
)
from .utils.validator import validate_yaml_against_schema


def _handle_run(args: argparse.Namespace) -> None:
    """Run the pipeline and print a JSON summary of emitted outputs."""
    args.out.mkdir(parents=True, exist_ok=True)
    tracker = Tracker(args.tracker)
    result = run_pipeline(registry_path=args.registry, out_dir=args.out, tracker=tracker)
    tracker.save()
    print(
        json.dumps(
            {"status": "ok", "outputs": [str(p) for p in result.outputs]},
            indent=2,
        )
    )


def _handle_tracker_plan(tracker: Tracker, args: argparse.Namespace) -> None:
    """Handle plan subcommands (seed/list/mark/stats/add)."""
    if args.plan_cmd == "seed-docs":
        created = plan_seed_from_docs(tracker)
        tracker.save()
        print(json.dumps({"status": "ok", "created": created}, indent=2))
    elif args.plan_cmd == "seed-sbom-ast":
        created = plan_seed_from_sbom_ast(tracker)
        tracker.save()
        print(json.dumps({"status": "ok", "created": created}, indent=2))
    elif args.plan_cmd == "seed-state":
        created = plan_seed_from_state(tracker)
        tracker.save()
        print(json.dumps({"status": "ok", "created": created}, indent=2))
    elif args.plan_cmd == "list":
        tasks = plan_list(tracker)
        print(json.dumps({"status": "ok", "tasks": tasks}, indent=2))
    elif args.plan_cmd == "stats":
        stats = plan_stats(tracker)
        print(json.dumps({"status": "ok", "stats": stats}, indent=2))
    elif args.plan_cmd == "mark":
        ok = plan_mark_task(tracker, args.id, args.status)
        tracker.save()
        print(json.dumps({"status": "ok" if ok else "not_found"}, indent=2))
    elif args.plan_cmd == "add":
        task = plan_add_task(
            tracker,
            {
                "title": args.title,
                "domain": args.domain,
                "category": args.category,
                "priority": args.priority,
                "status": args.status,
                "rationale": args.rationale,
                "doc_ref": args.doc_ref,
            },
        )
        tracker.save()
        print(json.dumps({"status": "ok", "task": task}, indent=2))


def _handle_tracker(args: argparse.Namespace) -> None:
    """Handle tracker subcommands (verify/list/touch/plan)."""
    tr_path: Path = args.tracker
    tracker = Tracker(tr_path)
    if args.tracker_cmd == "verify":
        mismatches = compute_mismatches(tracker)
        print(json.dumps({"status": "ok", "mismatches": mismatches}, indent=2))
    elif args.tracker_cmd == "list":
        print(
            json.dumps(
                {"status": "ok", "files": tracker.files, "meta": tracker.meta},
                indent=2,
            )
        )
    elif args.tracker_cmd == "touch":
        for rel in list(tracker.files.keys()):
            path_obj = Path(rel)
            if path_obj.exists():
                tracker.track_file(path_obj)
        tracker.save()
        print(json.dumps({"status": "ok", "message": "tracker updated"}, indent=2))
    elif args.tracker_cmd == "plan":
        _handle_tracker_plan(tracker, args)


def _handle_registry(args: argparse.Namespace) -> None:
    """Validate identifier_systems.yaml and mappings.yaml against their schemas."""
    if args.registry_cmd == "validate":
        # Validate identifier_systems.yaml and mappings.yaml if present
        base = Path(__file__).parent / "registry"
        results: list[dict[str, str]] = []
        targets = [
            (
                base / "identifier_systems.yaml",
                base / "identifier_systems.schema.json",
            ),
            (base / "mappings.yaml", base / "mappings.schema.json"),
        ]
        for yml, schema in targets:
            if yml.exists() and schema.exists():
                try:
                    validate_yaml_against_schema(yml, schema)
                    results.append({"file": str(yml), "status": "ok"})
                except Exception as e:
                    results.append({"file": str(yml), "status": f"error: {e}"})
        print(json.dumps({"status": "ok", "results": results}, indent=2))


def _handle_profiles(args: argparse.Namespace) -> None:
    """Validate/apply/check profiles against build outputs."""
    if args.profiles_cmd == "validate":
        try:
            schema = Path(__file__).parent / "registry" / "profile.schema.json"
            validate_yaml_against_schema(args.file, schema)
            print(json.dumps({"status": "ok", "file": str(args.file)}, indent=2))
        except Exception as e:
            print(json.dumps({"status": "error", "error": str(e)}, indent=2))
    elif args.profiles_cmd == "apply":
        try:
            schema = Path(__file__).parent / "registry" / "profile.schema.json"
            validate_yaml_against_schema(args.file, schema)
            # For now, applying a profile means evaluating it and returning result.
            result = evaluate_profile(args.file, Path("build"))
            print(json.dumps({"status": "ok", "result": result}, indent=2))
        except Exception as e:
            print(json.dumps({"status": "error", "error": str(e)}, indent=2))
    elif args.profiles_cmd == "check":
        try:
            schema = Path(__file__).parent / "registry" / "profile.schema.json"
            validate_yaml_against_schema(args.file, schema)
            result = evaluate_profile(args.file, Path("build"))
            print(json.dumps({"status": "ok", "result": result}, indent=2))
        except Exception as e:
            print(json.dumps({"status": "error", "error": str(e)}, indent=2))


def _handle_fetcher(args: argparse.Namespace) -> None:
    """Offline-first fetcher helpers: HTTP, pin/verify, HTML table scraper, GraphQL."""
    if args.fetcher_cmd == "get":
        path = fetch(args.url, args.cache, offline=args.offline)
        print(
            json.dumps(
                {
                    "status": "ok",
                    "cached": path is not None,
                    "path": str(path) if path else "",
                },
                indent=2,
            )
        )
    elif args.fetcher_cmd == "scrape-table":
        rows = extract_table_rows(args.file)
        print(json.dumps({"status": "ok", "rows": rows}, indent=2))
    elif args.fetcher_cmd == "pin":
        key = fetch_pin(args.url, args.cache)
        print(json.dumps({"status": "ok", "key": key}, indent=2))
    elif args.fetcher_cmd == "verify":
        ok = fetch_verify(args.url, args.cache, args.key)
        print(json.dumps({"status": "ok", "valid": ok}, indent=2))
    elif args.fetcher_cmd == "graphql":
        path = graphql_fetch(args.url, args.query, args.cache, offline=args.offline)
        print(
            json.dumps(
                {
                    "status": "ok",
                    "cached": path is not None,
                    "path": str(path) if path else "",
                },
                indent=2,
            )
        )


def main() -> None:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(prog="ufsa-v2", description="UFSA v2 Engine")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Run the ingestion-mapping-emission pipeline")
    run.add_argument(
        "--registry",
        type=Path,
        required=True,
        help="Path to pointer registry YAML",
    )
    run.add_argument("--out", type=Path, default=Path("build"), help="Output directory")
    run.add_argument(
        "--tracker",
        type=Path,
        default=Path("tracker.json"),
        help="Tracker file path",
    )

    # Tracker utilities
    tr = sub.add_parser("tracker", help="Tracker utilities")
    tr_sub = tr.add_subparsers(dest="tracker_cmd", required=True)
    tr_verify = tr_sub.add_parser("verify", help="Verify tracked file hashes vs filesystem")
    tr_verify.add_argument("--tracker", type=Path, default=Path("tracker.json"))
    tr_list = tr_sub.add_parser("list", help="List tracked files and hashes")
    tr_list.add_argument("--tracker", type=Path, default=Path("tracker.json"))
    tr_touch = tr_sub.add_parser("touch", help="Recompute hashes for currently tracked files and save")
    tr_touch.add_argument("--tracker", type=Path, default=Path("tracker.json"))

    # plan subcommands
    tr_plan = tr_sub.add_parser("plan", help="Plan management utilities")
    plan_sub = tr_plan.add_subparsers(dest="plan_cmd", required=True)
    for subcmd in (
        "seed-docs",
        "seed-state",
        "seed-sbom-ast",
        "list",
        "stats",
        "mark",
        "add",
    ):
        p = plan_sub.add_parser(subcmd)
        p.add_argument("--tracker", type=Path, default=Path("tracker.json"))
        if subcmd == "mark":
            p.add_argument("id", type=int)
            p.add_argument("status", choices=["todo", "in-progress", "done", "blocked"])
        if subcmd == "add":
            p.add_argument("title", type=str)
            p.add_argument("--domain", default="infrastructure")
            p.add_argument("--category", default="feature")
            p.add_argument("--priority", default="medium")
            p.add_argument("--status", default="todo")
            p.add_argument("--rationale", default="")
            p.add_argument("--doc-ref", dest="doc_ref", default="")

    # Registry utilities
    reg = sub.add_parser("registry", help="Registry utilities (identifier/mappings)")
    reg_sub = reg.add_subparsers(dest="registry_cmd", required=True)
    reg_sub.add_parser("validate", help="Validate on-disk registries")

    # Profiles utilities
    prof = sub.add_parser("profiles", help="Profiles and overlays")
    prof_sub = prof.add_subparsers(dest="profiles_cmd", required=True)
    prof_validate = prof_sub.add_parser("validate", help="Validate a profile YAML")
    prof_validate.add_argument("file", type=Path)
    prof_apply = prof_sub.add_parser("apply", help="Apply a profile (stub)")
    prof_apply.add_argument("file", type=Path)
    prof_check = prof_sub.add_parser("check", help="Check outputs against profile (stub)")
    prof_check.add_argument("file", type=Path)

    # Fetcher utilities
    fet = sub.add_parser("fetcher", help="Offline-first fetcher and simple scraper")
    fet_sub = fet.add_subparsers(dest="fetcher_cmd", required=True)
    fet_get = fet_sub.add_parser("get", help="Fetch a URL with cache")
    fet_get.add_argument("url", type=str)
    fet_get.add_argument("--cache", type=Path, default=Path(".cache"))
    fet_get.add_argument("--offline", action="store_true")
    fet_scrape = fet_sub.add_parser("scrape-table", help="Extract first table rows from an HTML file")
    fet_scrape.add_argument("file", type=Path)
    fet_pin = fet_sub.add_parser("pin", help="Return cache key for URL if cached")
    fet_pin.add_argument("url", type=str)
    fet_pin.add_argument("--cache", type=Path, default=Path(".cache"))
    fet_verify = fet_sub.add_parser("verify", help="Verify a cache key for URL")
    fet_verify.add_argument("url", type=str)
    fet_verify.add_argument("key", type=str)
    fet_verify.add_argument("--cache", type=Path, default=Path(".cache"))
    fet_graphql = fet_sub.add_parser("graphql", help="Fetch a GraphQL query with cache")
    fet_graphql.add_argument("url", type=str)
    fet_graphql.add_argument("query", type=str)
    fet_graphql.add_argument("--cache", type=Path, default=Path(".cache"))
    fet_graphql.add_argument("--offline", action="store_true")

    args = parser.parse_args()

    if args.command == "run":
        _handle_run(args)
    elif args.command == "tracker":
        _handle_tracker(args)
    elif args.command == "registry":
        _handle_registry(args)
    elif args.command == "profiles":
        _handle_profiles(args)
    elif args.command == "fetcher":
        _handle_fetcher(args)


if __name__ == "__main__":  # pragma: no cover
    main()
