"""Custom exceptions for aviation GIS tools."""


class AviationGisError(Exception):
    """Base exception for aviation_gis_tools errors."""


class UnsupportedUnitError(AviationGisError):
    """Raised when a unit is not supported."""


class InvalidNumberError(AviationGisError):
    """Raised when a value cannot be interpreted as a valid number."""


class NonPositiveNumberError(InvalidNumberError):
    """Raised when a number is not greater than zero."""


class VincentyConvergenceError(AviationGisError):
    """Raised when Vincenty's iterative solution does not converge."""


class UnsupportedEllipsoidError(AviationGisError):
    """Raised when ellipsoid used for calculation is not supported."""
