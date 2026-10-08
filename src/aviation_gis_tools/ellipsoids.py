"""Ellipsoids used for geodesic calculations."""


from dataclasses import dataclass

from .exceptions import UnsupportedEllipsoidError


@dataclass(frozen=True)
class Ellipsoid:
    """Reference ellipsoid parameters.

    Attributes:
        a: Semi-major axis in metres.
        b: Semi-minor axis in metres.
    """

    a: float
    b: float

    @property
    def f(self) -> float:
        """Flattening of the ellipsoid."""
        return (self.a - self.b) / self.a

WGS72 = Ellipsoid(
    a=6378135.0,
    b=6356750.52
)

WGS84 = Ellipsoid(
    a=6378137.0,
    b=6356752.3141
)

_ELLIPSOIDS: dict[str, Ellipsoid] = {
    "WGS72": WGS72,
    "WGS84": WGS84
}


def get_ellipsoid(name: str) -> Ellipsoid:
    """Return a registered ellipsoid by name.

    Args:
        name: Ellipsoid name, e.g. ``"WGS84"``.

    Raises:
        ValueError: If the ellipsoid is not registered.
    """
    try:
        return _ELLIPSOIDS[name.upper()]
    except KeyError:
        raise UnsupportedEllipsoidError(f"Unknown ellipsoid: {name!r}")
