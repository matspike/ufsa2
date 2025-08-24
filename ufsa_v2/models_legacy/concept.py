from __future__ import annotations

from pydantic import BaseModel, Field


class ConceptScheme(BaseModel):
    """A SKOS-like concept scheme."""

    id: str = Field(..., description="Stable scheme identifier")
    label: str = Field(..., description="Human-readable scheme label")
    uri: str | None = Field(None, description="Canonical scheme URI, if known")
    governing_body: str | None = Field(None, description="Standards body or source organization")


class Concept(BaseModel):
    """A normalized concept within a scheme."""

    id: str = Field(..., description="Stable concept identifier")
    pref_label: str = Field(..., description="Preferred label for the concept")
    definition: str | None = Field(None, description="Definition or note")
    notation: str | None = Field(None, description="Short code or notation, when applicable")
    scheme_uri: str | None = Field(None, description="URI of the scheme this concept belongs to")
