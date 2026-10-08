"""Geodesic calculations on reference ellipsoids.

This module provides Vincenty's direct geodesic solution for calculating
an endpoint from an initial coordinate, azimuth, and distance.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .ellipsoids import Ellipsoid, WGS84
from .exceptions import VincentyConvergenceError


@dataclass(frozen=True)
class Coordinate:
    """Geographic coordinate in decimal degrees."""

    latitude: float
    longitude: float


_MAX_ITERATIONS = 100
_CONVERGENCE_TOLERANCE = 1e-12



def vincenty_direct(
    origin: Coordinate,
    azimuth: float,
    distance: float,
    ellipsoid: Ellipsoid = WGS84,
) -> Coordinate:
    """Calculate a destination coordinate using Vincenty's direct solution.

    Args:
        origin: Starting coordinate in decimal degrees.
        azimuth: Initial bearing in decimal degrees.
        distance: Distance from the origin in metres.
        ellipsoid: Reference ellipsoid to use.

    Returns:
        Destination coordinate in decimal degrees.

    Raises:
        VincentyConvergenceError: If the iterative solution fails to
            converge.
    """
    latitude1 = math.radians(origin.latitude)
    longitude1 = math.radians(origin.longitude)
    azimuth1 = math.radians(azimuth)

    a, b, f = ellipsoid.a, ellipsoid.b, ellipsoid.f

    sin_azimuth1 = math.sin(azimuth1)
    cos_azimuth1 = math.cos(azimuth1)

    # Reduced latitude.
    tan_u1 = (1.0 - f) * math.tan(latitude1)
    cos_u1 = 1.0 / math.sqrt(1.0 + tan_u1 * tan_u1)
    sin_u1 = tan_u1 * cos_u1

    # Angular distance on the sphere from the equator to the initial point.
    sigma1 = math.atan2(tan_u1, cos_azimuth1)

    # Azimuth of the geodesic at the equator.
    sin_alpha = cos_u1 * sin_azimuth1
    cos_sq_alpha = 1.0 - sin_alpha * sin_alpha

    u_sq = cos_sq_alpha * (a * a - b * b) / (b * b)

    A = 1.0 + (
        u_sq
        / 16384.0
        * (
            4096.0
            + u_sq * (-768.0 + u_sq * (320.0 - 175.0 * u_sq))
        )
    )

    B = (
        u_sq
        / 1024.0
        * (
            256.0
            + u_sq * (-128.0 + u_sq * (74.0 - 47.0 * u_sq))
        )
    )

    sigma = distance / (b * A)

    for _ in range(_MAX_ITERATIONS):
        cos_2sigma_m = math.cos(2.0 * sigma1 + sigma)
        sin_sigma = math.sin(sigma)
        cos_sigma = math.cos(sigma)

        delta_sigma = B * sin_sigma * (
            cos_2sigma_m
            + B
            / 4.0
            * (
                cos_sigma * (-1.0 + 2.0 * cos_2sigma_m**2)
                - B
                / 6.0
                * cos_2sigma_m
                * (-3.0 + 4.0 * sin_sigma**2)
                * (-3.0 + 4.0 * cos_2sigma_m**2)
            )
        )

        next_sigma = distance / (b * A) + delta_sigma

        if abs(next_sigma - sigma) <= _CONVERGENCE_TOLERANCE:
            sigma = next_sigma
            break

        sigma = next_sigma
    else:
        raise VincentyConvergenceError(
            "Vincenty's direct solution failed to converge"
        )

    # Recalculate values using the converged sigma.
    sin_sigma = math.sin(sigma)
    cos_sigma = math.cos(sigma)
    cos_2sigma_m = math.cos(2.0 * sigma1 + sigma)

    auxiliary = (
        sin_u1 * sin_sigma
        - cos_u1 * cos_sigma * cos_azimuth1
    )

    latitude2 = math.atan2(
        sin_u1 * cos_sigma
        + cos_u1 * sin_sigma * cos_azimuth1,
        (1.0 - f)
        * math.sqrt(sin_alpha**2 + auxiliary**2),
    )

    lambda_ = math.atan2(
        sin_sigma * sin_azimuth1,
        cos_u1 * cos_sigma
        - sin_u1 * sin_sigma * cos_azimuth1,
    )

    C = (
        f
        / 16.0
        * cos_sq_alpha
        * (4.0 + f * (4.0 - 3.0 * cos_sq_alpha))
    )

    L = lambda_ - (
        (1.0 - C)
        * f
        * sin_alpha
        * (
            sigma
            + C
            * sin_sigma
            * (
                cos_2sigma_m
                + C
                * cos_sigma
                * (-1.0 + 2.0 * cos_2sigma_m**2)
            )
        )
    )

    longitude2 = (
        longitude1 + L + 3.0 * math.pi
    ) % (2.0 * math.pi) - math.pi

    return Coordinate(
        latitude=math.degrees(latitude2),
        longitude=math.degrees(longitude2),
    )
