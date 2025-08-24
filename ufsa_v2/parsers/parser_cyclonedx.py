"""CycloneDX SBOM parser (fixture-backed).

Transforms a minimal CycloneDX JSON (components/dependencies) into a
``ConceptScheme`` with software component concepts and dependency relations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ufsa_v2.core_models import Concept, ConceptScheme
from ufsa_v2.utils.errors import FixtureURLRequiredError
from ufsa_v2.utils.tracker import Tracker


def parse(
    *,
    standard_id: str,
    name: str,
    governing_body: str,
    specification_url: str,
    concept_scheme_uri: str,
    fixtures_dir: str,
    tracker: Tracker,
):
    """Parse a CycloneDX SBOM into a ``ConceptScheme``.

    Expects a simplified JSON with keys: ``components`` (list) and
    ``dependencies`` (list). Each component should include at least ``name`` and
    ``version``; ``purl`` and ``description`` are optional but recommended.
    Dependencies reference component ``ref`` keys which default to ``purl`` or
    ``name@version``.
    """
    if not specification_url.startswith("fixtures://"):
        raise FixtureURLRequiredError()
    fixture_rel = specification_url.replace("fixtures://", "")
    fixture_path = Path(fixtures_dir) / fixture_rel
    tracker.track_file(fixture_path)

    data: dict[str, Any] = json.loads(fixture_path.read_text())
    scheme = ConceptScheme(id=standard_id, label=name)

    # Build concepts
    ref_to_concept_id: dict[str, str] = {}
    for comp in data.get("components", []) or []:
        name_val = str(comp.get("name", "")).strip()
        version = str(comp.get("version", "")).strip()
        purl = str(comp.get("purl", "")).strip()
        description = str(comp.get("description", "")).strip()
        # optional enrichments
        licenses = _collect_licenses(comp)
        hashes = _collect_hashes(comp)
        ext_refs = _collect_external_references(comp)

        raw_ref = str(comp.get("bom-ref", "")).strip()
        # prefer bom-ref, else purl, else name@version
        ref = (
            raw_ref
            or purl
            or (f"{name_val}@{version}" if name_val or version else name_val)
        )
        concept_id = f"{standard_id}:{ref or name_val or version}"
        c = Concept(
            id=concept_id,
            label=name_val or purl or ref,
            notes={
                "notation": version,
                "description": description,
                "purl": purl,
                "kind": "software_component",
                "licenses": (
                    ";".join([x for x in licenses if x]) if licenses else ""
                ),
                "hashes": ";".join(hashes) if hashes else "",
                "externalReferences": ";".join(ext_refs) if ext_refs else "",
            },
        )
        c.in_scheme = concept_scheme_uri
        scheme.concepts[c.id] = c
        if ref:
            ref_to_concept_id[ref] = c.id
        if purl:
            ref_to_concept_id.setdefault(purl, c.id)
        # also allow name@version lookup for dependencies lacking full purl
        if name_val or version:
            ref_to_concept_id.setdefault(f"{name_val}@{version}", c.id)

    # Dependencies: link as skos:related
    for dep in data.get("dependencies", []) or []:
        ref = str(dep.get("ref", "")).strip()
        src_id = ref_to_concept_id.get(ref)
        if not src_id:
            continue
        for tgt in dep.get("dependsOn", []) or []:
            tgt_id = ref_to_concept_id.get(str(tgt))
            if tgt_id and tgt_id not in scheme.concepts[src_id].related:
                scheme.concepts[src_id].related.append(tgt_id)

    return scheme


def _collect_licenses(comp: dict[str, Any]) -> list[str]:
    result: list[str] = []
    for item in comp.get("licenses", []) or []:
        lic = item.get("license") or {}
        expr = item.get("expression")
        if expr:
            result.append(str(expr))
        elif lic:
            result.append(str(lic.get("id") or lic.get("name") or ""))
    return result


def _collect_hashes(comp: dict[str, Any]) -> list[str]:
    result: list[str] = []
    for h in comp.get("hashes", []) or []:
        alg = str(h.get("alg", "")).upper()
        val = str(h.get("content", ""))
        if alg and val:
            result.append(f"{alg}:{val}")
    return result


def _collect_external_references(comp: dict[str, Any]) -> list[str]:
    result: list[str] = []
    for er in comp.get("externalReferences", []) or []:
        url = str(er.get("url", "")).strip()
        if url:
            result.append(url)
    return result
