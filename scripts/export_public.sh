#!/usr/bin/env bash
set -euo pipefail

# Export a clean snapshot of the current repo (HEAD) into a sibling directory
# without any git history. By default, build/ outputs are NOT included because
# they are git-ignored. You can opt-in with --include-build and/or include
# sealed meta with --include-sealed.
#
# Usage:
#   scripts/export_public.sh [DEST_DIR] [--force] [--clean] [--include-build] [--include-sealed]
#
# Defaults:
#   DEST_DIR       ../public

DEST_DIR="${1:-}" || true
shift || true 2>/dev/null || true || true

FORCE=0
CLEAN=0
INC_BUILD=0
INC_SEALED=0
INC_DIST=0
INC_DOCS=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force) FORCE=1; shift;;
    --clean) CLEAN=1; shift;;
    --include-build) INC_BUILD=1; shift;;
  --include-sealed) INC_SEALED=1; shift;;
  --include-dist) INC_DIST=1; shift;;
  --include-docs) INC_DOCS=1; shift;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done

if [[ -z "${DEST_DIR}" ]]; then
  DEST_DIR="../public"
fi

mkdir -p "${DEST_DIR}"

# Handle cleaning or refusing to overwrite non-empty
if [[ ${CLEAN} -eq 1 ]]; then
  echo "🧹 Cleaning destination: ${DEST_DIR}"
  # Remove the directory entirely to ensure hidden files are also removed, then recreate
  rm -rf "${DEST_DIR}"
  mkdir -p "${DEST_DIR}"
fi

if [[ ${FORCE} -ne 1 ]]; then
  if [[ -n $(ls -A "${DEST_DIR}" 2>/dev/null || true) ]]; then
    echo "error: destination ${DEST_DIR} is not empty. Use --force or --clean." >&2
    exit 1
  fi
fi

echo "📦 Exporting tracked files from HEAD to ${DEST_DIR} (no git metadata)"
git archive --format=tar HEAD | tar -x -C "${DEST_DIR}"

if [[ ${INC_BUILD} -eq 1 ]]; then
  if [[ -d build ]]; then
    echo "➕ Including build/ outputs"
    mkdir -p "${DEST_DIR}/build"
    rsync -a --delete build/ "${DEST_DIR}/build/"
  else
    echo "warn: build/ not found; run the pipeline first to produce outputs" >&2
  fi
fi

if [[ ${INC_SEALED} -eq 1 ]]; then
  if [[ -d licensed_src_meta_sealed ]]; then
    echo "➕ Including sealed meta outputs"
    mkdir -p "${DEST_DIR}/licensed_src_meta_sealed"
    rsync -a licensed_src_meta_sealed/ "${DEST_DIR}/licensed_src_meta_sealed/"
  fi
  if [[ -f LICENSE_HASHES.md ]]; then
    cp -f LICENSE_HASHES.md "${DEST_DIR}/"
  fi
fi

if [[ ${INC_DIST} -eq 1 ]]; then
  if [[ -d dist ]]; then
    echo "➕ Including dist/ release artifacts"
    mkdir -p "${DEST_DIR}/dist"
    rsync -a dist/ "${DEST_DIR}/dist/"
  else
    echo "warn: dist/ not found; run 'make release' first to build release artifacts" >&2
  fi
fi

if [[ ${INC_DOCS} -eq 1 ]]; then
  if [[ -d site ]]; then
    echo "➕ Including site/ built documentation"
    mkdir -p "${DEST_DIR}/site"
    rsync -a site/ "${DEST_DIR}/site/"
  else
    echo "warn: site/ not found; run 'make docs' to build documentation" >&2
  fi
fi

echo "✅ Export complete: ${DEST_DIR}"
echo "Contents (top-level):"
ls -1 "${DEST_DIR}" | sed 's/^/  - /'
