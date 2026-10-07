"""Utilities for converting distance between supported aviation units."""


from dataclasses import dataclass, field
from enum import StrEnum

from .exceptions import UnsupportedUnitError
from .numbers import is_positive, parse_number


_METERS_PER_KILOMETER = 1_000
_METERS_PER_NAUTICAL_MILE = 1_852
_METERS_PER_FOOT = 0.3048
_METERS_PER_STATUTE_MILE = 1_609.344


class DistanceUnit(StrEnum):
    """Supported units for measuring distance.

    Attributes:
        M: Meters.
        KM: Kilometers.
        FT: Feet.
        NM: Nautical miles.
        SM: Statute miles.
    """

    M = "m"
    KM = "km"
    FT = "ft"
    NM = "nm"
    SM = "mi"


_DISTANCE_TO_METERS: dict[DistanceUnit, float] = {
    DistanceUnit.M: 1.0,
    DistanceUnit.KM: _METERS_PER_KILOMETER,
    DistanceUnit.FT: _METERS_PER_FOOT,
    DistanceUnit.NM: _METERS_PER_NAUTICAL_MILE,
    DistanceUnit.SM: _METERS_PER_STATUTE_MILE,
}


def convert_distance(
    value: float,
    from_unit: DistanceUnit,
    to_unit: DistanceUnit,
) -> float:
    """Convert a distance between supported distance units.

    :param value: Distance value to convert.
    :param from_unit: Unit of the input distance value.
    :param to_unit: Unit to convert the distance value to.
    :return: Converted distance value in ``to_unit``.
    :raises UnsupportedUnitError: If either unit is not supported.
    """
    if not isinstance(from_unit, DistanceUnit):
        raise UnsupportedUnitError(
            f"Unsupported distance unit: {from_unit!r}"
        )

    if not isinstance(to_unit, DistanceUnit):
        raise UnsupportedUnitError(
            f"Unsupported distance unit: {to_unit!r}"
        )
    return (
        value
        * _DISTANCE_TO_METERS[from_unit]
        / _DISTANCE_TO_METERS[to_unit]
    )


@dataclass(frozen=True)
class Distance:
    """Represent a distance.

    Attributes:
        value: Distance value as in source data (e.g. eAIP, NOTAM)
        unit: Unit in which the distance value is expressed.
        label: Label used when representing the distance (e.g. inner circle for defining restricted area in eAIP, NOTAM)
        value_num: Normalized distance value as a finite positive float.
    """
    value: int | float | str
    unit: DistanceUnit
    label: str
    value_num: float = field(init=False)

    def __post_init__(self) -> None:
        """Validate and normalize the distance value.

        :raises UnsupportedUnitError: If the distance unit is not supported.
        :raises InvalidNumberError: If the value cannot be parsed as a
            finite number.
        :raises NonPositiveNumberError: If the value is zero or negative.
        """
        if not isinstance(self.unit, DistanceUnit):
            raise UnsupportedUnitError(
                f"Unsupported distance unit: {self.unit!r}"
            )

        value_num = parse_number(self.value)
        is_positive(value_num)
        object.__setattr__(self, "value_num", value_num)

    def __str__(self) -> str:
        """Return a human-readable representation of the distance.

        :return: The distance label, value, and unit.
        """
        return f"{self.label}: {self.value} {self.unit}"

    def convert(self, to_unit: DistanceUnit) -> float:
        """Convert the distance to another unit.

        :param to_unit: The unit to convert the distance to.
        :return: The converted distance value.
        :raises UnsupportedUnitError: If ``to_unit`` is not a supported
        distance unit.
        """
        return convert_distance(value=self.value_num,
                                from_unit=self.unit,
                                to_unit=to_unit)


