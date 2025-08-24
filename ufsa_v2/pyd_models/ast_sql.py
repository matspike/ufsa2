from __future__ import annotations

from pydantic import BaseModel, Field


class DatabaseColumn(BaseModel):
    """A column within a database table."""

    name: str = Field(..., description="Column name")
    data_type: str | None = Field(None, description="Column data type, if known")


class ForeignKey(BaseModel):
    """A foreign key relationship between two tables/columns."""

    table: str = Field(..., description="Referencing (child) table name")
    column: str = Field(..., description="Referencing (child) column name")
    ref_table: str = Field(..., description="Referenced (parent) table name")
    ref_column: str = Field(..., description="Referenced (parent) column name")


class DatabaseTable(BaseModel):
    """A database table with columns and optional FKs."""

    name: str = Field(..., description="Table name")
    columns: list[DatabaseColumn] = Field(default_factory=list, description="Columns in the table")
    foreign_keys: list[ForeignKey] = Field(default_factory=list, description="Foreign key constraints")
