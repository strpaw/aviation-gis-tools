"""Custom exceptions for aviation GIS tools."""


class AviationGisError(Exception):
    """Base exception for aviation_gis_tools errors."""


class UnsupportedUnitError(AviationGisError):
    """Raised when a unit is not supported."""
