import math

import pytest

from aviation_gis_tools.exceptions import (
    InvalidNumberError,
    NonPositiveNumberError,
)
from aviation_gis_tools.numbers import is_positive, parse_number


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (10, 10.0),
        (10.5, 10.5),
        ("10", 10.0),
        ("10.5", 10.5),
        ("10,5", 10.5),
        (" 10.5 ", 10.5),
        (" 10,5 ", 10.5),
        (0, 0.0),
        (-10, -10.0),
    ],
)
def test_parse_number_returns_float(value, expected):
    assert parse_number(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        True,
        False,
        "abc",
        "",
        " ",
        "1.2.3",
        "1,2,3",
        object(),
        None,
    ],
)
def test_parse_number_rejects_invalid_values(value):
    with pytest.raises(InvalidNumberError):
        parse_number(value)


@pytest.mark.parametrize(
    "value",
    [
        math.nan,
        math.inf,
        -math.inf,
        "nan",
        "NaN",
        "inf",
        "Infinity",
        "-inf",
    ],
)
def test_parse_number_rejects_non_finite_values(value):
    with pytest.raises(InvalidNumberError):
        parse_number(value)


def test_parse_number_preserves_original_exception():
    with pytest.raises(InvalidNumberError) as exc_info:
        parse_number("invalid")

    assert isinstance(exc_info.value.__cause__, ValueError)


@pytest.mark.parametrize(
    "value",
    [
        0.1,
        1,
        10.5,
        1_000_000,
    ],
)
def test_is_positive_accepts_positive_numbers(value):
    assert is_positive(value) is None


@pytest.mark.parametrize(
    "value",
    [
        0,
        -1,
        -0.1,
        -100,
    ],
)
def test_is_positive_rejects_non_positive_numbers(value):
    with pytest.raises(NonPositiveNumberError):
        is_positive(value)


def test_is_positive_error_message():
    with pytest.raises(
        NonPositiveNumberError,
        match=r"Value must be a positive number: 0",
    ):
        is_positive(0)
