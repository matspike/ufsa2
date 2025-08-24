# UFSA v2 Makefile
# Wraps uv, pipeline, and tracker utilities for convenience.

.PHONY: help sync install dev test lint lint-fix fmt type check run pipeline clean clean-build clean-py \
	tracker-verify tracker-list tracker-touch plan-seed-docs plan-seed-state plan-list plan-stats seal seal-clean \
	version package-sealed package-verify package-list package-with-build package-verify-with-build package-list-with-build release

help:
	@echo "Targets:"
	@echo "  sync           - Sync dependencies with uv"
	@echo "  install        - Alias of sync"
	@echo "  dev            - Run lint, type, and tests"
	@echo "  test           - Run unit tests"
	@echo "  lint           - Run ruff checks"
	@echo "  lint-fix       - Run ruff with --fix"
	@echo "  fmt            - Run ruff formatter"
	@echo "  type           - Run static type checks"
	@echo "  check          - Run lint, type, tests"
	@echo "  run/pipeline   - Run the UFSA pipeline"
	@echo "  tracker-verify - Verify tracked files match current hashes"
	@echo "  tracker-list   - List tracked files and meta"
	@echo "  tracker-touch  - Recompute hashes for tracked files and save"
	@echo "  plan-seed-docs - Seed plan tasks from Docs 1/2"
	@echo "  plan-seed-state- Seed plan tasks from current tracker state (what's done)"
	@echo "  plan-list      - List plan tasks"
	@echo "  plan-stats     - Show plan completion stats"
	@echo "  clean          - Remove build artifacts and caches"
	@echo "  seal           - Run license sealing into licensed_src_* dirs"
	@echo "  seal-clean     - Remove license sealing output dirs and report"
	@echo "  version        - Print project version and expected tag (v<version>)"
	@echo "  package-sealed - Create dist/sealed-meta.tgz from dist.whitelist.txt (runs seal first)"
	@echo "  package-verify - Verify required files exist inside dist/sealed-meta.tgz"
	@echo "  package-list   - List first N entries in dist/sealed-meta.tgz"
	@echo "  package-with-build - Create dist/sealed-meta-with-build.tgz incl. SBOM/AST outputs (runs pipeline + seal)"
	@echo "  package-verify-with-build - Verify required files incl. SBOM/AST exist in dist/sealed-meta-with-build.tgz"
	@echo "  package-list-with-build - List first N entries in dist/sealed-meta-with-build.tgz"
	@echo "  release        - Run pipeline, seal, package-with-build, verify"
	@echo "  docs           - Build MkDocs site"
	@echo "  docs-serve     - Serve MkDocs locally"
	@echo "  export-public  - Copy tracked files to ../public (no git), optional build/sealed"

sync install:
	uv sync

dev: lint type test

test:
	uv run -q pytest -q

lint:
	uv run -q ruff check

lint-fix:
	uv run -q ruff check --fix

fmt:
	uv run -q ruff format

type:
	uv run -q ty check

check: lint-fix type test

run pipeline:
	uv run -q ufsa-v2 run --registry ufsa_v2/registry/pointer_registry.yaml --out build --tracker tracker.json

tracker-verify:
	uv run -q ufsa-v2 tracker verify --tracker tracker.json

tracker-list:
	uv run -q ufsa-v2 tracker list --tracker tracker.json

tracker-touch:
	uv run -q ufsa-v2 tracker touch --tracker tracker.json

plan-seed-docs:
	uv run -q ufsa-v2 tracker plan seed-docs --tracker tracker.json

plan-seed-state:
	uv run -q ufsa-v2 tracker plan seed-state --tracker tracker.json

plan-list:
	uv run -q ufsa-v2 tracker plan list --tracker tracker.json

plan-stats:
	uv run -q ufsa-v2 tracker plan stats --tracker tracker.json

clean: clean-build clean-py
	rm -rf .pytest_cache .ruff_cache
	rm -f LICENSE_HASHES.md

clean-build:
	rm -rf build dist *.egg-info licensed_src_content_sealed licensed_src_meta_sealed

clean-py:
	find . -name "__pycache__" -type d -exec rm -rf {} +

seal:
	uv run SEAL_LICENSE.py

seal-clean:
	rm -rf licensed_src_content_sealed licensed_src_meta_sealed LICENSE_HASHES.md

version:
	uv run -q python scripts/seal_package.py version

package-sealed: seal
	uv run -q python scripts/seal_package.py package --whitelist dist.whitelist.txt --out dist/sealed-meta.tgz

package-verify:
	uv run -q python scripts/seal_package.py verify --archive dist/sealed-meta.tgz

package-list:
	uv run -q python scripts/seal_package.py list --archive dist/sealed-meta.tgz --limit 80

# Create an archive that includes sealed sources and selected build artifacts (SBOM/AST)
package-with-build: pipeline seal
	uv run -q python scripts/seal_package.py package --whitelist dist.whitelist.with_build.txt --out dist/sealed-meta-with-build.tgz

package-verify-with-build:
	uv run -q python scripts/seal_package.py verify --archive dist/sealed-meta-with-build.tgz \
		--expect build/software_components.csv --expect build/database_schemas.csv \
		--expect build/cyclonedx_example.concepts.csv --expect build/internal_dw_schema.concepts.csv

package-list-with-build:
	uv run -q python scripts/seal_package.py list --archive dist/sealed-meta-with-build.tgz --limit 80

# Convenience: end-to-end release bundle with build artifacts
release: package-with-build package-verify-with-build package-list-with-build

docs:
	uv run -q mkdocs build -q

docs-serve:
	uv run -q mkdocs serve -a 127.0.0.1:8000

export-public: release docs
	bash scripts/export_public.sh ../public --clean --include-build --include-sealed --include-dist --include-docs
