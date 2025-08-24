from __future__ import annotations

from pydantic import BaseModel, Field


class IdentifierSystem(BaseModel):
    """Registry entry for identifier systems (e.g., ISIN, CUSIP)."""

    id: str = Field(..., description="Identifier system ID")
    name: str = Field(..., description="System name")
    authority: str | None = Field(None, description="Governing authority")
    uri: str | None = Field(None, description="Canonical URI for the system")
    description: str | None = Field(None, description="Short description")
