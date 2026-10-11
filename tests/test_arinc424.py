import pytest

from aviation_gis_tools.arinc424 import (
    ARINC424Quadrant,
    _FORMAT_LONGITUDE_EQUAL_GRATER_HUNDRED,
    _FORMAT_LONGITUDE_LESS_HUNDRED,
    encode,
    decode,
    get_arinc424_quadrant,
    get_format,
    longitude_suffix,
)
from aviation_gis_tools.exceptions import InvalidARINC424FormatError


@pytest.mark.parametrize(
    ("lon", "expected"),
    [
        (0, "00"),
        (1, "01"),
        (5, "05"),
        (9, "09"),
        (10, "10"),
        (99, "99"),
        (100, "00"),
        (105, "05"),
        (180, "80"),
    ],
)
def test_longitude_suffix(lon: int, expected: str) -> None:
    assert longitude_suffix(lon) == expected


@pytest.mark.parametrize(
    ("lon", "lat", "expected"),
    [
        (10, 20, ARINC424Quadrant.NE),
        (-10, 20, ARINC424Quadrant.NW),
        (-10, -20, ARINC424Quadrant.SW),
        (10, -20, ARINC424Quadrant.SE),
        (0, 20, ARINC424Quadrant.NE),
        (10, 0, ARINC424Quadrant.NE),
        (0, -20, ARINC424Quadrant.SE),
        (-10, 0, ARINC424Quadrant.NW),
        (0, 0, ARINC424Quadrant.NE),
    ],
)
def test_get_arinc424_quadrant(
    lon: int,
    lat: int,
    expected: ARINC424Quadrant,
) -> None:
    assert get_arinc424_quadrant(lon, lat) == expected


@pytest.mark.parametrize(
    ("lon", "expected"),
    [
        (0, _FORMAT_LONGITUDE_LESS_HUNDRED),
        (5, _FORMAT_LONGITUDE_LESS_HUNDRED),
        (-99, _FORMAT_LONGITUDE_LESS_HUNDRED),
        (99, _FORMAT_LONGITUDE_LESS_HUNDRED),
        (100, _FORMAT_LONGITUDE_EQUAL_GRATER_HUNDRED),
        (-100, _FORMAT_LONGITUDE_EQUAL_GRATER_HUNDRED),
        (180, _FORMAT_LONGITUDE_EQUAL_GRATER_HUNDRED),
        (-180, _FORMAT_LONGITUDE_EQUAL_GRATER_HUNDRED),
    ],
)
def test_get_format(lon: int, expected: str) -> None:
    assert get_format(lon) == expected


@pytest.mark.parametrize(
    ("lat", "lon", "expected"),
    [
        (20, 5, "2005E"),
        (20, -5, "2005N"),
        (-20, -5, "2005W"),
        (-20, 5, "2005S"),
        (0, 0, "000E"),
        (45, 99, "4599E"),
        (45, 100, "45E00"),
        (45, 105, "45E05"),
        (-45, -100, "45W00"),
        (-45, 180, "45S80"),
    ],
)
def test_encode(lat: int, lon: int, expected: str) -> None:
    assert encode(lat=lat, lon=lon) == expected

@pytest.mark.parametrize(
    ("arinc424", "expected"),
    [
        # Longitude less than 100 degrees
        ("2005E", (20.0, 5.0)),
        ("2005N", (20.0, -5.0)),
        ("2005W", (-20.0, -5.0)),
        ("2005S", (-20.0, 5.0)),
        ("0000E", (0.0, 0.0)),
        ("9000E", (90.0, 0.0)),
        # Longitude equal to or greater than 100 degrees
        ("45E00", (45.0, 100.0)),
        ("45E05", (45.0, 105.0)),
        ("45W00", (-45.0, -100.0)),
        ("45S80", (-45.0, 180.0)),
        ("45N80", (45.0, -180.0)),
        ("00E80", (0.0, 180.0)),
    ],
)
def test_decode(arinc424: str, expected: tuple[float, float]) -> None:
    assert decode(arinc424) == expected


@pytest.mark.parametrize(
    "arinc424",
    [
        "",
        "2005",
        "2005X",
        "200E",
        "ABCDE",
        "20005E",
        "2005EE",
        "2005e",
        " 2005E",
        "2005E ",
    ],
)
def test_decode_invalid_format(arinc424: str) -> None:
    with pytest.raises(InvalidARINC424FormatError):
        decode(arinc424)
