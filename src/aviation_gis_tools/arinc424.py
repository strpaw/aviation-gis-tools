"""Utilities for decoding/encoding ARINC 424 full degrees coordinates"""


from enum import StrEnum
import re
from typing import NamedTuple


from .exceptions import InvalidARINC424FormatError


_FORMAT_LONGITUDE_LESS_HUNDRED = "{lat}{lon}{quadrant}"
_FORMAT_LONGITUDE_EQUAL_GRATER_HUNDRED = "{lat}{quadrant}{lon}"

_REGEX_ARINC424 = {
    'LONGITUDE_LESS_HUNDRED': re.compile(
        r'''^(?P<lat>[0-8]\d|90)
             (?P<lon>[0-7]\d|80)
             (?P<letter>[NSEW])$
        ''', re.VERBOSE
    ),
    'LONGITUDE_EQUAL_GRATER_HUNDRED': re.compile(
        r'''(?P<lat>[0-8]\d|90)
        (?P<letter>[NSEW])
        (?P<lon>[0-7]\d|80)
        ''', re.VERBOSE)
}


class ARINC424Quadrant(StrEnum):
    """Supported quadrants in ARINC 424 full degrees code format.

    Attributes:
        NW: Northwest quadrant.
        NE: Northeast quadrant.
        SW: Southwest quadrant.
        SE: Southeast quadrant.
    """

    NW = "N"
    NE = "E"
    SW = "W"
    SE = "S"


class Hemisphere(StrEnum):
    """Cardinal hemispheres used to indicate geographic direction.

    Attributes:
        NORTH: Northern hemisphere.
        SOUTH: Southern hemisphere.
        EAST: Eastern hemisphere.
        WEST: Western hemisphere.
    """
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"

class CoordinateHemispheres(NamedTuple):
    latitude: Hemisphere
    longitude: Hemisphere


_ARINC424_QUADRANT_TO_HEMISPHERES: dict[
    ARINC424Quadrant, CoordinateHemispheres
] = {
    ARINC424Quadrant.NW: CoordinateHemispheres(
        latitude=Hemisphere.NORTH,
        longitude=Hemisphere.WEST,
    ),
    ARINC424Quadrant.NE: CoordinateHemispheres(
        latitude=Hemisphere.NORTH,
        longitude=Hemisphere.EAST,
    ),
    ARINC424Quadrant.SW: CoordinateHemispheres(
        latitude=Hemisphere.SOUTH,
        longitude=Hemisphere.WEST,
    ),
    ARINC424Quadrant.SE: CoordinateHemispheres(
        latitude=Hemisphere.SOUTH,
        longitude=Hemisphere.EAST,
    ),
}


def longitude_suffix(lon: int) -> str:
    """Return the last two digits of the longitude, zero-padded if necessary.

    :param lon: Longitude
    :return: A two-digit string representing the longitude modulo 100
    """
    return f"{lon % 100:02d}"


def get_arinc424_quadrant(lon: int, lat: int) -> ARINC424Quadrant:
    """Determine the ARINC424 quadrant from longitude and latitude.

    :param lon: Longitude
    :param lat: Latitude
    :return: The corresponding ARINC 424 quadrant.
    """
    if lat >= 0:
        return ARINC424Quadrant.NE if lon >= 0 else ARINC424Quadrant.NW

    return ARINC424Quadrant.SE if lon >= 0 else ARINC424Quadrant.SW


def get_format(lon: int) -> str:
    """Return ARINC 424 full degrees format based on quadrant in which coordinates are given.

    :param lon: longitude
    :return: The format corresponding to the longitude range.
    """
    if abs(lon) < 100:
        return _FORMAT_LONGITUDE_LESS_HUNDRED
    return _FORMAT_LONGITUDE_EQUAL_GRATER_HUNDRED


def encode(lat: int,
           lon: int) -> str:
    """Encode latitude and longitude into the ARINC 424 full-degrees format.

    :param lat: Latitude
    :param lon: Longitude
    :return: The encoded coordinate string
    """
    quadrant = get_arinc424_quadrant(lon, lat)
    latitude = abs(lat)
    longitude = longitude_suffix(abs(lon))
    return get_format(lon).format(lat=latitude, lon=longitude, quadrant=quadrant)


def decode(arinc424: str) -> tuple[float, float]:
    """Decode an ARINC 424 full-degrees coordinate code into longitude and latitude.

    :param arinc424: Coordinate code in ARINC 424 full-degrees format
    :return: A tuple containing (latitude, longitude) in decimal degrees.
    Raises:
        ValueError: If the input does not match a supported ARINC 424 format.
    """
    for code_type, rgx in _REGEX_ARINC424.items():
        match = rgx.match(arinc424)
        if not match:
            continue

        lat = float(match.group('lat'))
        lon = float(match.group('lon'))
        letter = match.group('letter')
        letter_pos = arinc424.find(letter)
        if letter_pos == 2:
            lon += 100
        hemispheres = _ARINC424_QUADRANT_TO_HEMISPHERES.get(letter)
        lat = -lat if hemispheres.latitude == Hemisphere.SOUTH else lat
        lon = -lon if hemispheres.longitude == Hemisphere.WEST else lon
        return lat, lon

    raise InvalidARINC424FormatError("Invalid ARINC424 format")
