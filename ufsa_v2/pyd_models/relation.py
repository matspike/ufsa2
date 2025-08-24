from __future__ import annotations

from pydantic import BaseModel, Field


class Relation(BaseModel):
    """A semantic relation between two concepts (SKOS-like)."""

    subject_id: str = Field(..., description="Concept ID of the subject")
    predicate: str = Field(..., description="Predicate IRI or compact term")
    object_id: str = Field(..., description="Concept ID of the object")
