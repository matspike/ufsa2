from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Concept:
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
    id: str
    label: str
    concepts: dict[str, Concept] = field(default_factory=dict)


@dataclass
class UFSAStandard:
    standard_id: str
    name: str
    governing_body: str
    specification_url: str
    data_format: str
    parser_module: str
    concept_scheme_uri: str


@dataclass
class Registry:
    standards: list[UFSAStandard]


@dataclass
class PipelineResult:
    outputs: list[str]
