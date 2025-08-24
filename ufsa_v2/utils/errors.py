"""Custom exceptions for UFSA v2."""


class FixtureURLRequiredError(ValueError):
    """Raised when a parser expects a fixtures:// URL during bootstrap."""
