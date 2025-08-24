#!/usr/bin/env python
"""
Seal packaging utility

Subcommands:
  - package: Create dist/sealed-meta.tgz from dist.whitelist.txt (after make seal)
  - verify:  Verify expected files exist inside dist/sealed-meta.tgz
  - list:    List first N entries in the archive (default 60)
  - version: Print repo version and expected tag

This script intentionally avoids external deps and uses Python stdlib only.
"""

from __future__ import annotations

import argparse
import glob
import os
import shutil
import sys
import tarfile
import tempfile
from pathlib import PurePosixPath


def read_version(pyproject_path: str = "pyproject.toml") -> str | None:
    try:
        import tomllib  # Python 3.11+

        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)
        return data.get("project", {}).get("version")
    except Exception:
        return None


def package(whitelist_path: str, out_path: str) -> None:
    if not os.path.exists(whitelist_path):
        print(
            f"error: whitelist file not found: {whitelist_path}",
            file=sys.stderr,
        )
        sys.exit(2)

    # Stage files into a temp directory based on whitelist
    stage = tempfile.mkdtemp(prefix="seal_pkg_")
    included = 0
    with open(whitelist_path, encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            # Support recursive globs like **
            matched = glob.glob(line, recursive=True)
            if not matched:
                # It's okay to have a non-matching pattern, but log it for visibility
                print(f"warn: pattern matched no files: {line}")
                continue
            for path in matched:
                if not os.path.exists(path):
                    continue
                dest = os.path.join(stage, path)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                if os.path.isdir(path):
                    shutil.copytree(path, dest, dirs_exist_ok=True)
                else:
                    shutil.copy2(path, dest)
                included += 1

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with tarfile.open(out_path, "w:gz") as tf:
        tf.add(stage, arcname=".")

    print(f"created: {out_path} (staged {included} entries)")


def verify(archive_path: str, extra_expected: list[str] | None = None) -> None:
    if not os.path.exists(archive_path):
        print(f"error: archive not found: {archive_path}", file=sys.stderr)
        sys.exit(2)
    with tarfile.open(archive_path, "r:gz") as tf:
        names = {str(PurePosixPath(m.name).as_posix().lstrip("./")) for m in tf.getmembers()}

    # Minimal expectations: top-level legal docs and at least one sealed source
    expected = [
        "LICENSE",
        "LICENSE_HASHES.md",
        "README.md",
        "licensed_src_meta_sealed/ufsa_v2/utils/scraper.py",
    ]
    if extra_expected:
        expected.extend(extra_expected)
    ok = True
    for e in expected:
        present = e in names
        print(("FOUND: " if present else "MISSING: ") + e)
        ok = ok and present
    if not ok:
        sys.exit(1)


def list_contents(archive_path: str, limit: int = 60) -> None:
    if not os.path.exists(archive_path):
        print(f"error: archive not found: {archive_path}", file=sys.stderr)
        sys.exit(2)
    with tarfile.open(archive_path, "r:gz") as tf:
        for i, m in enumerate(tf.getmembers()):
            if i >= limit:
                break
            print(m.name)


def print_version() -> None:
    version = read_version() or "unknown"
    print("version:", version)
    if version != "unknown":
        print("expected tag:", f"v{version}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="seal_package")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_pack = sub.add_parser("package", help="Create sealed archive using dist.whitelist.txt")
    p_pack.add_argument("--whitelist", default="dist.whitelist.txt")
    p_pack.add_argument("--out", default=os.path.join("dist", "sealed-meta.tgz"))

    p_ver = sub.add_parser("verify", help="Verify required files exist in the sealed archive")
    p_ver.add_argument("--archive", default=os.path.join("dist", "sealed-meta.tgz"))
    p_ver.add_argument(
        "--expect",
        dest="expect",
        action="append",
        help="Additional expected file path(s) inside the archive",
    )

    p_ls = sub.add_parser("list", help="List archive contents (first N entries)")
    p_ls.add_argument("--archive", default=os.path.join("dist", "sealed-meta.tgz"))
    p_ls.add_argument("-n", "--limit", type=int, default=60)

    sub.add_parser("version", help="Print project version and expected tag")

    args = parser.parse_args(argv)
    if args.cmd == "package":
        package(args.whitelist, args.out)
        return 0
    if args.cmd == "verify":
        verify(args.archive, args.expect)
        return 0
    if args.cmd == "list":
        list_contents(args.archive, args.limit)
        return 0
    if args.cmd == "version":
        print_version()
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
