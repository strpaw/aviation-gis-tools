"""Utilities for converting speeds between supported aviation units."""
from enum import StrEnum

from .exceptions import UnsupportedUnitError

_METERS_PER_KILOMETER = 1_000
_SECONDS_PER_HOUR = 3_600
_METERS_PER_NAUTICAL_MILE = 1_852


class SpeedUnit(StrEnum):
    """Supported units for measuring speed.

    Attributes:
        MPS: Meters per second.
        KMH: Kilometers per hour.
        KT: Knots.
    """

    MPS = "m/s"
    KMH = "km/h"
    KT = "kt"


_SPEED_TO_MPS: dict[SpeedUnit, float] = {
    SpeedUnit.MPS: 1.0,
    SpeedUnit.KMH: _METERS_PER_KILOMETER / _SECONDS_PER_HOUR,
    SpeedUnit.KT: _METERS_PER_NAUTICAL_MILE / _SECONDS_PER_HOUR,
}


def convert_speed(
    value: float,
    from_unit: SpeedUnit,
    to_unit: SpeedUnit,
) -> float:
    """Convert a speed between supported speed units.

    :param value: Speed value to convert.
    :param from_unit: Unit of the input speed value.
    :param to_unit: Unit to convert the speed value to.
    :return: Converted speed value in ``to_unit``.
    :raises UnsupportedUnitError: If either unit is not supported.
    """
    if not isinstance(from_unit, SpeedUnit):
        raise UnsupportedUnitError(f"Unsupported speed unit: {from_unit}")

    if not isinstance(to_unit, SpeedUnit):
        raise UnsupportedUnitError(f"Unsupported speed unit: {to_unit}")

    return value * _SPEED_TO_MPS[from_unit] / _SPEED_TO_MPS[to_unit]

