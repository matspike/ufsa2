# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
# Copyright 2025 Matthew Spike — Repo: https://github.com/matspike/ufsa2 — LinkedIn: https://www.linkedin.com/in/matspike
#
# This file is part of ufsa2.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# --- INTEGRITY SEAL ---
# Initial Hash (sha256-orig): 207d2cbf2cda770f87b3cecd70a090efc91d104f818db5980c49c23f519cba4d
# Sealed Hash  (sha256-sealed-v1): e68071b5f0e65ec9de61dffe70db9b8195daecc566604a83ace9b296224c620f
#
"""
License Sealing and Verification Script (Self-Sealing & UV-Aware Version).

This script performs a two-stage cryptographic sealing process to embed license
and integrity information directly into source files. It is designed to find
and seal itself, ensuring the integrity of the tooling alongside the source code.

It is also aware of `uv` script headers (`# /// script ... # ///`) and will
preserve them at the top of the file, injecting the license seal after them.

Rationale for the Two-Stage Seal:
1.  Content Seal (v1): The first seal takes a hash of the original,
    unmodified source file (initial_hash) and embeds it into the license
    header. This creates a verifiable link to the original content.

2.  Meta Seal (v2): The second seal takes the hash of the entire
    content-sealed file (sealed_hash_v1) and embeds it alongside the
    initial_hash. This final version creates a self-verifying artifact.
"""

from __future__ import annotations

import hashlib
import shutil
import textwrap
import tomllib
from datetime import datetime
from pathlib import Path
from typing import NamedTuple

# --- TEMPLATE FOR THE DYNAMIC HEADER ---
LICENSE_HEADER_TEMPLATE = """\
# {copyright_line}
#
# This file is part of {project_name}.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     {license_url}
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# --- INTEGRITY SEAL ---
# Initial Hash (sha256-orig): {initial_hash}
# Sealed Hash  (sha256-sealed-v1): {sealed_hash_v1}
#
"""


class FileSealRecord(NamedTuple):
    """A record of a file's path and its full hash chain."""

    relative_path: Path
    initial_hash: str
    sealed_hash_v1: str
    sealed_hash_v2: str


def calculate_sha256(data: bytes) -> str:
    """Calculates the SHA-256 hash of a byte string."""
    return hashlib.sha256(data).hexdigest()


def _split_uv_and_strip_license_header(
    original_full_bytes: bytes,
) -> tuple[bytes, bytes]:
    """Return (uv_header_bytes, core_content_bytes) for this file.

    - Preserves any leading uv script header block.
    - Strips any existing license/comment header following the uv header to make
      in-place sealing idempotent for this script.
    """
    uv_header_bytes = b""
    main_content_bytes = original_full_bytes
    uv_end_marker = b"# ///\n"
    if original_full_bytes.strip().startswith(b"# /// script"):
        try:
            header_end_index = original_full_bytes.index(uv_end_marker) + len(
                uv_end_marker
            )
            uv_header_bytes = original_full_bytes[:header_end_index]
            main_content_bytes = original_full_bytes[header_end_index:]
        except ValueError:
            # No end marker found; treat whole file as main content.
            main_content_bytes = original_full_bytes
    # Attempt to strip an existing license header comment block (lines starting with '#')
    try:
        text = main_content_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return uv_header_bytes, main_content_bytes
    lines = text.splitlines(keepends=True)
    i = 0
    while i < len(lines):
        line = lines[i]
        # Skip comment lines and leading empty lines
        if line.startswith("#") or not line.strip():
            i += 1
            continue
        break
    core_text = "".join(lines[i:])
    return uv_header_bytes, core_text.encode("utf-8")


def find_python_files(paths: list[Path]) -> list[Path]:
    """
    Find all unique .py files from a list of directories and/or files.
    - Accepts both directories and files
    - Skips common generated/virtualenv directories
    - Returns sorted unique absolute paths
    """
    EXCLUDE_DIRS = {
        ".git",
        ".venv",
        "venv",
        "env",
        "build",
        "dist",
        "licensed_src_content_sealed",
        "licensed_src_meta_sealed",
        "__pycache__",
        ".pytest_cache",
        ".ruff_cache",
    }
    py_files_set: set[Path] = set()

    def should_skip(p: Path) -> bool:
        return any(part in EXCLUDE_DIRS for part in p.parts)

    for entry in paths:
        if entry.is_file() and entry.suffix == ".py":
            if not should_skip(entry):
                py_files_set.add(entry.resolve())
            continue
        if not entry.is_dir():
            print(f"Warning: Not found or not a dir/file, skipping: {entry}")
            continue
        for path in entry.rglob("*.py"):
            if not should_skip(path):
                py_files_set.add(path.resolve())
    return sorted(py_files_set)


def get_project_meta(project_root: Path) -> dict:
    """
    Dynamically loads project metadata from pyproject.toml and NOTICE.
    """
    year = datetime.now().year
    meta: dict[str, str] = {
        "project_name": "Unknown Project",
        "license_url": "http://www.apache.org/licenses/LICENSE-2.0",
    }
    pyproject_path = project_root / "pyproject.toml"
    if pyproject_path.exists():
        with pyproject_path.open("rb") as f:
            pyproject_data = tomllib.load(f)
        project_info = pyproject_data.get("project", {})
        meta["project_name"] = project_info.get("name", meta["project_name"])
        urls = project_info.get("urls", {})
        meta["repository"] = urls.get("Repository", "")
        meta["linkedin"] = urls.get("LinkedIn", "")
        authors = project_info.get("authors", [])
        if authors:
            author = authors[0]
            author_name = author.get("name", "Anonymous")
            base = f"Copyright {year} {author_name}"
            extras: list[str] = []
            if meta.get("repository"):
                extras.append(f"Repo: {meta['repository']}")
            if meta.get("linkedin"):
                extras.append(f"LinkedIn: {meta['linkedin']}")
            suffix = (" — " + " — ".join(extras)) if extras else ""
            meta["copyright_line"] = base + suffix
    # Fallback to NOTICE first line if authors were not present
    if "copyright_line" not in meta:
        notice_path = project_root / "NOTICE"
        if notice_path.exists():
            first = (
                notice_path.read_text(encoding="utf-8").splitlines()[0].strip()
            )
            if first:
                meta["copyright_line"] = first
            else:
                meta["copyright_line"] = f"Copyright {year}"
        else:
            meta["copyright_line"] = f"Copyright {year}"
    return meta


def generate_hashes_markdown(
    records: list[FileSealRecord], output_file: Path
) -> None:
    """Generates a Markdown file with a table of the full hash chain."""
    header = textwrap.dedent(
        """\
        # License Sealing Hash Report

        This document records the SHA-256 hash chain for each source file after applying
        the two-stage license sealing process.

        - Initial Hash: Hash of the original, unmodified file.
        - Sealed Hash (v1): Hash of the file after injecting the Initial Hash into the header.
        - Sealed Hash (v2): Hash of the file after injecting both hashes into the header (the final artifact).

        | File Path | Initial Hash (Original) | Sealed Hash (v1) | Sealed Hash (v2 - Final) |
        |-----------|-------------------------|------------------|--------------------------|
    """
    )
    rows = [
        f"| `{r.relative_path}` | `{r.initial_hash[:12]}` | `{r.sealed_hash_v1[:12]}` | `{r.sealed_hash_v2[:12]}` |"
        for r in records
    ]
    output_file.write_text(header + "\n".join(rows) + "\n", encoding="utf-8")
    print(f"✅ Successfully generated hash report at: {output_file}")


def main() -> None:
    """Main script execution."""
    # --- CONFIGURATION ---
    # Target only project source and tests by default; include this script explicitly.
    source_dirs_to_scan = ["ufsa_v2", "tests"]
    include_self = True
    output_dir_v1_name = "licensed_src_content_sealed"
    output_dir_v2_name = "licensed_src_meta_sealed"
    hash_report_file_name = "LICENSE_HASHES.md"
    # --- END CONFIGURATION ---

    project_root = Path(__file__).parent.resolve()
    source_paths = [project_root / d for d in source_dirs_to_scan]
    if include_self:
        source_paths.append(project_root / Path(__file__).name)
    output_path_v1 = project_root / output_dir_v1_name
    output_path_v2 = project_root / output_dir_v2_name
    hash_report_path = project_root / hash_report_file_name

    for path in [output_path_v1, output_path_v2]:
        if path.exists():
            print(f"🧹 Removing existing output directory: {path}")
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)

    print("🔍 Finding Python files...")
    python_files = find_python_files(source_paths)
    if not python_files:
        print("No Python files found. Exiting.")
        return

    print("⚙️ Loading project metadata...")
    project_meta = get_project_meta(project_root)
    print(f"  - Project: {project_meta['project_name']}")
    print(f"  - Copyright: {project_meta['copyright_line']}")

    print(
        f"Found {len(python_files)} Python files to process. Starting two-stage seal..."
    )
    seal_records: list[FileSealRecord] = []

    for source_file in python_files:
        relative_path = source_file.relative_to(project_root)
        print(f"  - Processing: {relative_path}")

        # --- Stage 0: Get Original Content and Hash ---
        original_full_bytes = source_file.read_bytes()
        # For this script, make in-place sealing idempotent by stripping any
        # existing license header when computing hashes and content to seal.
        is_self = (
            source_file.resolve()
            == (project_root / Path(__file__).name).resolve()
        )
        if is_self:
            uv_header_bytes, main_content_bytes = (
                _split_uv_and_strip_license_header(original_full_bytes)
            )
            initial_hash = calculate_sha256(
                uv_header_bytes + main_content_bytes
            )
        else:
            # Detect and separate a `uv` script header if it exists.
            uv_header_bytes = b""
            main_content_bytes = original_full_bytes
            uv_end_marker = b"# ///\n"
            if original_full_bytes.strip().startswith(b"# /// script"):
                try:
                    header_end_index = original_full_bytes.index(
                        uv_end_marker
                    ) + len(uv_end_marker)
                    uv_header_bytes = original_full_bytes[:header_end_index]
                    main_content_bytes = original_full_bytes[header_end_index:]
                except ValueError:
                    # No end marker found, treat as a normal file.
                    pass
            initial_hash = calculate_sha256(original_full_bytes)

        # --- Stage 1: Content Seal ---
        header_v1_text = LICENSE_HEADER_TEMPLATE.format(
            **project_meta,
            initial_hash=initial_hash,
            sealed_hash_v1="<pending>",
        )
        sealed_content_v1_bytes = (
            uv_header_bytes
            + header_v1_text.encode("utf-8")
            + main_content_bytes
        )
        sealed_hash_v1 = calculate_sha256(sealed_content_v1_bytes)

        dest_file_v1 = output_path_v1 / relative_path
        dest_file_v1.parent.mkdir(parents=True, exist_ok=True)
        dest_file_v1.write_bytes(sealed_content_v1_bytes)

        # --- Stage 2: Meta Seal ---
        header_v2_text = LICENSE_HEADER_TEMPLATE.format(
            **project_meta,
            initial_hash=initial_hash,
            sealed_hash_v1=sealed_hash_v1,
        )
        sealed_content_v2_bytes = (
            uv_header_bytes
            + header_v2_text.encode("utf-8")
            + main_content_bytes
        )
        sealed_hash_v2 = calculate_sha256(sealed_content_v2_bytes)

        dest_file_v2 = output_path_v2 / relative_path
        dest_file_v2.parent.mkdir(parents=True, exist_ok=True)
        dest_file_v2.write_bytes(sealed_content_v2_bytes)

        # --- Record Keeping ---
        seal_records.append(
            FileSealRecord(
                relative_path=relative_path,
                initial_hash=initial_hash,
                sealed_hash_v1=sealed_hash_v1,
                sealed_hash_v2=sealed_hash_v2,
            )
        )

        # For this script only: write the sealed v2 content back in place so the
        # process is "sealed at the top". This is idempotent because we strip any
        # existing license header when computing hashes and content.
        if is_self:
            source_file.write_bytes(sealed_content_v2_bytes)
            print(f"📝 Self-sealed in place: {relative_path}")

    generate_hashes_markdown(seal_records, hash_report_path)


if __name__ == "__main__":  # pragma: no cover
    main()
