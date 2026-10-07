import math

import pytest

from aviation_gis_tools.ellipsoids import WGS84
from aviation_gis_tools.ellipsoid_calc import (
    Coordinate,
    vincenty_direct,
)
from aviation_gis_tools.exceptions import UnsupportedEllipsoidError



@pytest.mark.parametrize(
    (
        "latitude",
        "longitude",
        "azimuth",
        "distance",
        "expected_latitude",
        "expected_longitude",
    ),
    [
        # North from the equator.
        (
            0.0,
            0.0,
            0.0,
            10_000.0,
            0.09043694695356691,
            0.0,
        ),
        # East from the equator.
        (
            0.0,
            0.0,
            90.0,
            10_000.0,
            5.5376636427532604e-18,
            0.08983152841248263,
        ),
        # South from the equator.
        (
            0.0,
            0.0,
            180.0,
            1_000.0,
            -0.009043694727216058,
            0.0,
        ),
        # West from the equator.
        (
            0.0,
            0.0,
            270.0,
            10_000.0,
            -1.661299092825978e-17,
            -0.08983152841248263,
        ),
        # 360 degrees should behave like 0 degrees.
        (
            0.0,
            0.0,
            360.0,
            100_000.0,
            0.9043687229398173,
            0.0,
        ),
        # Arbitrary real-world-ish case.
        (
            -32.5,
            137.5,
            127.5,
            243_855.411,
            -33.8212028224309,
            139.58969185673908,
        ),
    ],
)
def test_vincenty_direct(
    latitude,
    longitude,
    azimuth,
    distance,
    expected_latitude,
    expected_longitude,
):
    result = vincenty_direct(
        origin=Coordinate(
            latitude=latitude,
            longitude=longitude,
        ),
        azimuth=azimuth,
        distance=distance,
        ellipsoid=WGS84,
    )

    assert math.isclose(
        result.latitude,
        expected_latitude,
        rel_tol=0.0,
        abs_tol=1e-10,
    )

    assert math.isclose(
        result.longitude,
        expected_longitude,
        rel_tol=0.0,
        abs_tol=1e-10,
    )


def test_vincenty_direct_defaults_to_wgs84():
    origin = Coordinate(latitude=0.0, longitude=0.0)

    result_default = vincenty_direct(
        origin=origin,
        azimuth=0.0,
        distance=10_000.0,
    )

    result_explicit = vincenty_direct(
        origin=origin,
        azimuth=0.0,
        distance=10_000.0,
        ellipsoid=WGS84,
    )

    assert math.isclose(
        result_default.latitude,
        result_explicit.latitude,
        rel_tol=0.0,
        abs_tol=1e-10,
    )
    assert math.isclose(
        result_default.longitude,
        result_explicit.longitude,
        rel_tol=0.0,
        abs_tol=1e-10,
    )
