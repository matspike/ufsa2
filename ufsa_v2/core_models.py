"""Core runtime data models for the UFSA engine.

These dataclasses represent the minimal SKOS-inspired runtime model used by
parsers and emitters. They are deliberately lightweight and free of Pydantic
validation to keep the ingestion/emit pipeline fast and dependency-light.

For rich, documentation-oriented models (with validation), see
``ufsa_v2.pyd_models`` which are used by the docs site (mkdocstrings) and not
by the runtime pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Concept:
    """A single SKOS-like concept within a concept scheme.

    Attributes:
        id: Globally unique identifier for the concept. Often scoped as
            "<scheme_id>:<local_id>".
        label: Preferred human-readable label (akin to skos:prefLabel).
        notes: Arbitrary key/value annotations (definition/description,
            notation/code, data_type, purl, etc.).
        broader: Concept IDs that this concept is a narrower child of
            (skos:broader).
        narrower: Concept IDs that are narrower children of this concept
            (skos:narrower).
        related: Concept IDs that are related (skos:related).
        in_scheme: Canonical URI of the owning concept scheme.
        exact_match: External URIs that are exact matches (skos:exactMatch).
        close_match: External URIs that are close matches (skos:closeMatch).
        broad_match: External URIs that are broader matches (skos:broadMatch).
        narrow_match: External URIs that are narrower matches (skos:narrowMatch).
        related_match: External URIs that are related matches (skos:relatedMatch).
    """

    id: str
    label: str
    notes: dict[str, str] = field(default_factory=dict)
    broader: list[str] = field(default_factory=list)
    narrower: list[str] = field(default_factory=list)
    related: list[str] = field(default_factory=list)
    in_scheme: str | None = None
    # SKOS mapping predicates (cross-scheme or external)
    exact_match: list[str] = field(default_factory=list)
    close_match: list[str] = field(default_factory=list)
    broad_match: list[str] = field(default_factory=list)
    narrow_match: list[str] = field(default_factory=list)
    related_match: list[str] = field(default_factory=list)


@dataclass
class ConceptScheme:
    """A named collection of concepts belonging to a standard.

    Attributes:
        id: Short identifier for the scheme (e.g., "iso_4217").
        label: Human-friendly name for the scheme.
        concepts: Mapping of concept_id -> Concept.
    """

    id: str
    label: str
    concepts: dict[str, Concept] = field(default_factory=dict)


@dataclass
class UFSAStandard:
    """Pointer registry entry describing how to ingest a standard.

    Attributes:
        standard_id: Short, unique identifier for the standard.
        name: Display name of the standard.
        governing_body: Organization or authority that publishes the standard.
        specification_url: Location of the specification (fixtures:// or URL).
        data_format: Source data format (csv, json, rdf, sql, etc.).
        parser_module: Python module path that implements ``parse``.
        concept_scheme_uri: Canonical URI to assign to members via ``in_scheme``.
    """

    standard_id: str
    name: str
    governing_body: str
    specification_url: str
    data_format: str
    parser_module: str
    concept_scheme_uri: str


@dataclass
class Registry:
    """A collection of standards to ingest in a pipeline run."""

    standards: list[UFSAStandard]


@dataclass
class PipelineResult:
    """Results from a pipeline run.

    Attributes:
        outputs: Paths to emitted artifacts tracked by the ``Tracker``.
    """

    outputs: list[str]
