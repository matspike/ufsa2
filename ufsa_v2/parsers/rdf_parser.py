"""RDF/SKOS parser (fixture-backed).

Loads an RDF file and extracts SKOS Concepts and relations into the runtime
model. Supports labels, definitions, notations, altLabels, and mapping
predicates when present.
"""

from __future__ import annotations

from pathlib import Path

from rdflib import RDF, RDFS, SKOS, Graph

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
) -> ConceptScheme:
    """Parse SKOS concepts and relations from an RDF file into a ConceptScheme."""
    if not specification_url.startswith("fixtures://"):
        raise FixtureURLRequiredError()
    fixture_rel = specification_url.replace("fixtures://", "")
    fixture_path = Path(fixtures_dir) / fixture_rel
    tracker.track_file(fixture_path)

    g = Graph()
    g.parse(fixture_path)

    scheme = ConceptScheme(id=standard_id, label=name)

    # Collect SKOS Concepts with labels and enrich with SKOS properties
    for s in g.subjects(RDF.type, SKOS.Concept):
        pref_label = g.value(s, SKOS.prefLabel) or g.value(s, RDFS.label)
        if not pref_label:
            # If no label, skip to keep output meaningful
            continue
        cid = f"{standard_id}:{s}"
        c = Concept(id=cid, label=str(pref_label))
        c.in_scheme = concept_scheme_uri

        # Notes: definition, notation; include altLabel for context if present
        definition = g.value(s, SKOS.definition)
        if definition:
            c.notes["description"] = str(definition)
        # Collect all notations (join when multiple)
        notations = [str(n) for n in g.objects(s, SKOS.notation)]
        if notations:
            c.notes["notation"] = ";".join(notations)
        # altLabels (optional, semicolon-separated)
        alt_labels = [str(al) for al in g.objects(s, SKOS.altLabel)]
        if alt_labels:
            c.notes["altLabel"] = ";".join(alt_labels)

        scheme.concepts[c.id] = c

    _wire_relations_and_mappings(g, standard_id, scheme)

    if not scheme.concepts:
        # fallback: add the scheme node itself
        c = Concept(id=f"{standard_id}:{concept_scheme_uri}", label=name)
        c.in_scheme = concept_scheme_uri
        scheme.concepts[c.id] = c

    return scheme


def _wire_relations_and_mappings(
    g: Graph, standard_id: str, scheme: ConceptScheme
) -> None:
    for s in g.subjects(RDF.type, SKOS.Concept):
        src_id = f"{standard_id}:{s}"
        src = scheme.concepts.get(src_id)
        if not src:
            continue
        _add_relations(g, s, standard_id, src)
        _add_mappings(g, s, src)


def _add_relations(g: Graph, s, standard_id: str, src: Concept) -> None:  # type: ignore[name-defined]
    for o in g.objects(s, SKOS.broader):
        src.broader.append(f"{standard_id}:{o}")
    for o in g.objects(s, SKOS.narrower):
        src.narrower.append(f"{standard_id}:{o}")
    for o in g.objects(s, SKOS.related):
        src.related.append(f"{standard_id}:{o}")


def _add_mappings(g: Graph, s, src: Concept) -> None:  # type: ignore[name-defined]
    for o in g.objects(s, SKOS.exactMatch):
        src.exact_match.append(str(o))
    for o in g.objects(s, SKOS.closeMatch):
        src.close_match.append(str(o))
    for o in g.objects(s, SKOS.broadMatch):
        src.broad_match.append(str(o))
    for o in g.objects(s, SKOS.narrowMatch):
        src.narrow_match.append(str(o))
    for o in g.objects(s, SKOS.relatedMatch):
        src.related_match.append(str(o))
