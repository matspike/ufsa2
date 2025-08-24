from __future__ import annotations

from pydantic import BaseModel, Field


class Relation(BaseModel):
    """A semantic relation between two concepts, typically SKOS-like.

    Example predicates: "skos:broader", "skos:narrower", "skos:related",
    "skos:exactMatch", "skos:closeMatch", "skos:broadMatch", "skos:narrowMatch",
    "skos:relatedMatch".
    """

    subject_id: str = Field(..., description="Concept ID of the subject")
    predicate: str = Field(..., description="Predicate IRI or compact term")
    object_id: str = Field(..., description="Concept ID of the object")
