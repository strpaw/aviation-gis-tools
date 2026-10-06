import pytest

from aviation_gis_tools.exceptions import UnsupportedUnitError
from aviation_gis_tools.speed import SpeedUnit, convert_speed

@pytest.mark.parametrize(
    ("value", "from_unit", "to_unit", "expected"),
    [
        (1.0, SpeedUnit.MPS, SpeedUnit.MPS, 1.0),
        (1.0, SpeedUnit.KMH, SpeedUnit.KMH, 1.0),
        (1.0, SpeedUnit.KT, SpeedUnit.KT, 1.0),
        (1.0, SpeedUnit.KMH, SpeedUnit.MPS, 1000 / 3600),
        (1.0, SpeedUnit.MPS, SpeedUnit.KMH, 3.6),
        (36.0, SpeedUnit.KMH, SpeedUnit.MPS, 10.0),
        (10.0, SpeedUnit.MPS, SpeedUnit.KMH, 36.0),
        (1.0, SpeedUnit.KT, SpeedUnit.MPS, 1852 / 3600),
        (1.0, SpeedUnit.MPS, SpeedUnit.KT, 3600 / 1852),
        (10.0, SpeedUnit.KT, SpeedUnit.KMH, (10 * 1852) / 1000),
        (18.52, SpeedUnit.KMH, SpeedUnit.KT, 10.0),
    ],
)
def test_convert_speed(
    value: float,
    from_unit: SpeedUnit,
    to_unit: SpeedUnit,
    expected: float,
) -> None:
    assert convert_speed(value, from_unit, to_unit) == pytest.approx(expected)


@pytest.mark.parametrize("unit", list(SpeedUnit))
def test_convert_speed_same_unit(unit: SpeedUnit) -> None:
    value = 123.456

    assert convert_speed(value, unit, unit) == pytest.approx(value)


@pytest.mark.parametrize(
    "value",
    [0.0, -10.0, 123456.789],
)
def test_convert_speed_values(value: float) -> None:
    # Converting through m/s should preserve the original value.
    for unit in SpeedUnit:
        result = convert_speed(
            convert_speed(value, unit, SpeedUnit.MPS),
            SpeedUnit.MPS,
            unit,
        )
        assert result == pytest.approx(value)


@pytest.mark.parametrize(
    "invalid_unit",
    [
        "m/s",
        "km/h",
        "kt",
        "mph",
        None,
        1,
        object(),
    ],
)
def test_convert_speed_rejects_invalid_from_unit(invalid_unit) -> None:
    with pytest.raises(
        UnsupportedUnitError,
        match=r"Unsupported speed unit:",
    ):
        convert_speed(10.0, invalid_unit, SpeedUnit.MPS)


@pytest.mark.parametrize(
    "invalid_unit",
    [
        "m/s",
        "km/h",
        "kt",
        "mph",
        None,
        1,
        object(),
    ],
)
def test_convert_speed_rejects_invalid_to_unit(invalid_unit) -> None:
    with pytest.raises(
        UnsupportedUnitError,
        match=r"Unsupported speed unit:",
    ):
        convert_speed(10.0, SpeedUnit.MPS, invalid_unit)
