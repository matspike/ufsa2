from __future__ import annotations

from pydantic import BaseModel, Field


class SoftwareComponent(BaseModel):
    """Represents a software component from CycloneDX SBOM."""

    id: str = Field(..., description="Stable ID (bom-ref or derived)")
    name: str = Field(..., description="Component name")
    version: str | None = Field(None, description="Version string")
    purl: str | None = Field(None, description="Package URL if available")
    licenses: list[str] = Field(default_factory=list, description="License identifiers")
    hashes: list[str] = Field(default_factory=list, description="Component hashes (e.g., SHA-256)")
    external_references: list[str] = Field(
        default_factory=list,
        description="External reference URLs (homepage, repo, docs)",
    )
