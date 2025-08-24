from __future__ import annotations

from pydantic import BaseModel, Field


class Mapping(BaseModel):
    """Curated mapping between identifier systems and/or concepts."""

    source: str = Field(..., description="Source concept or identifier system ID")
    target: str = Field(..., description="Target concept or identifier system ID")
    predicate: str = Field(..., description="Relation/predicate that describes the mapping")
    note: str | None = Field(None, description="Optional note or rationale")
