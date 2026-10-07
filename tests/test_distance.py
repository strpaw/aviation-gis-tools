import pytest

from aviation_gis_tools.distance import (
    Distance,
    DistanceUnit,
    convert_distance,
)
from aviation_gis_tools.exceptions import (
    InvalidNumberError,
    NonPositiveNumberError,
    UnsupportedUnitError,
)


@pytest.mark.parametrize(
    ("value", "from_unit", "to_unit", "expected"),
    [
        (1, DistanceUnit.M, DistanceUnit.M, 1.0),
        (1, DistanceUnit.KM, DistanceUnit.M, 1_000.0),
        (1, DistanceUnit.M, DistanceUnit.KM, 0.001),
        (1, DistanceUnit.NM, DistanceUnit.M, 1_852.0),
        (1, DistanceUnit.M, DistanceUnit.NM, 1 / 1_852),
        (1, DistanceUnit.FT, DistanceUnit.M, 0.3048),
        (1, DistanceUnit.M, DistanceUnit.FT, 1 / 0.3048),
        (1, DistanceUnit.SM, DistanceUnit.M, 1_609.344),
        (1, DistanceUnit.M, DistanceUnit.SM, 1 / 1_609.344),
        (10, DistanceUnit.KM, DistanceUnit.NM, 10_000 / 1_852),
    ],
)
def test_convert_distance(
    value,
    from_unit,
    to_unit,
    expected,
):
    result = convert_distance(value, from_unit, to_unit)

    assert result == pytest.approx(expected)


@pytest.mark.parametrize(
    "unit",
    [
        "m",
        "km",
        "nm",
        "ft",
        "mi",
        None,
        123,
    ],
)
def test_convert_distance_rejects_unsupported_from_unit(unit):
    with pytest.raises(
        UnsupportedUnitError,
        match=r"Unsupported distance unit:",
    ):
        convert_distance(1, unit, DistanceUnit.M)


@pytest.mark.parametrize(
    "unit",
    [
        "m",
        "km",
        "nm",
        "ft",
        "mi",
        None,
        123,
    ],
)
def test_convert_distance_rejects_unsupported_to_unit(unit):
    with pytest.raises(
        UnsupportedUnitError,
        match=r"Unsupported distance unit:",
    ):
        convert_distance(1, DistanceUnit.M, unit)


def test_distance_accepts_integer_value():
    distance = Distance(
        value=10,
        unit=DistanceUnit.KM,
        label="Runway length",
    )

    assert distance.value == 10
    assert distance.value_num == 10.0


def test_distance_accepts_float_value():
    distance = Distance(
        value=10.5,
        unit=DistanceUnit.KM,
        label="Runway length",
    )

    assert distance.value == 10.5
    assert distance.value_num == 10.5


def test_distance_accepts_numeric_string():
    distance = Distance(
        value="10.5",
        unit=DistanceUnit.KM,
        label="Runway length",
    )

    assert distance.value == "10.5"
    assert distance.value_num == 10.5


def test_distance_accepts_decimal_comma():
    distance = Distance(
        value="10,5",
        unit=DistanceUnit.KM,
        label="Runway length",
    )

    assert distance.value_num == 10.5


def test_distance_strips_numeric_string():
    distance = Distance(
        value=" 10.5 ",
        unit=DistanceUnit.KM,
        label="Runway length",
    )

    assert distance.value_num == 10.5


@pytest.mark.parametrize(
    "value",
    [
        "",
        " ",
        "abc",
        "10.2.3",
        "10,2,3",
        None,
        object(),
        True,
        False,
    ],
)
def test_distance_rejects_invalid_value(value):
    with pytest.raises(InvalidNumberError):
        Distance(
            value=value,
            unit=DistanceUnit.KM,
            label="Distance",
        )


@pytest.mark.parametrize(
    "value",
    [
        0,
        -1,
        -0.1,
        "0",
        "-1",
        "0,0",
    ],
)
def test_distance_rejects_non_positive_value(value):
    with pytest.raises(NonPositiveNumberError):
        Distance(
            value=value,
            unit=DistanceUnit.KM,
            label="Distance",
        )


@pytest.mark.parametrize(
    "unit",
    [
        "m",
        "km",
        "nm",
        "ft",
        "mi",
        None,
        123,
    ],
)
def test_distance_rejects_unsupported_unit(unit):
    with pytest.raises(
        UnsupportedUnitError,
        match=r"Unsupported distance unit:",
    ):
        Distance(
            value=10,
            unit=unit,
            label="Distance",
        )


def test_distance_str():
    distance = Distance(
        value="10.5",
        unit=DistanceUnit.KM,
        label="Runway length",
    )

    assert str(distance) == "Runway length: 10.5 km"


@pytest.mark.parametrize(
    ("distance_unit", "to_unit", "expected"),
    [
        (DistanceUnit.M, DistanceUnit.KM, 0.001),
        (DistanceUnit.KM, DistanceUnit.M, 1_000.0),
        (DistanceUnit.NM, DistanceUnit.M, 1_852.0),
        (DistanceUnit.FT, DistanceUnit.M, 0.3048),
        (DistanceUnit.SM, DistanceUnit.M, 1_609.344),
    ],
)
def test_distance_convert(distance_unit, to_unit, expected):
    distance = Distance(
        value=1,
        unit=distance_unit,
        label="Distance",
    )

    assert distance.convert(to_unit) == pytest.approx(expected)


def test_distance_convert_rejects_unsupported_unit():
    distance = Distance(
        value=10,
        unit=DistanceUnit.KM,
        label="Distance",
    )

    with pytest.raises(
        UnsupportedUnitError,
        match=r"Unsupported distance unit:",
    ):
        distance.convert("m")


def test_distance_is_immutable():
    distance = Distance(
        value=10,
        unit=DistanceUnit.KM,
        label="Distance",
    )

    with pytest.raises(AttributeError):
        distance.value = 20


def test_distance_value_num_is_normalized_to_float():
    distance = Distance(
        value=10,
        unit=DistanceUnit.KM,
        label="Distance",
    )

    assert isinstance(distance.value_num, float)
