import math

import pytest

from aviation_gis_tools.ellipsoids import (
    Ellipsoid,
    WGS72,
    WGS84,
    get_ellipsoid
)
from aviation_gis_tools.exceptions import UnsupportedEllipsoidError


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("WGS84", WGS84),
        ("wgs84", WGS84),
        ("WGS72", WGS72),
        ("wgs72", WGS72),
    ],
)
def test_get_ellipsoid(name, expected):
    assert get_ellipsoid(name) is expected


def test_get_ellipsoid_unknown_name():
    with pytest.raises(UnsupportedEllipsoidError, match="Unknown ellipsoid"):
        get_ellipsoid("UNKNOWN")