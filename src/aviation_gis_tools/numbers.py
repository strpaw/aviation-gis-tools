"""Numeric parsing and validation utilities for aviation GIS tools."""


import math
from typing import TypeAlias

from .exceptions import (
    InvalidNumberError,
    NonPositiveNumberError
)

Number: TypeAlias = int | float | str


def parse_number(value: Number) -> float:
    """Parse a number from an int, float, or decimal string.

    :param value: The value to parse into a finite floating-point number.
    :return: The parsed value as a finite float.
    :raises InvalidNumberError: If the value cannot be converted into a number
        or is not finite.
    """
    if isinstance(value, bool):
        raise InvalidNumberError(
            f"Value must be a number: {value!r}"
        )

    if isinstance(value, (int, float)):
        result = float(value)
    elif isinstance(value, str):
        text = value.strip().replace(",", ".")
        try:
            result = float(text)
        except ValueError as exc:
            raise InvalidNumberError(
                f"Value must be a number: {value!r}"
            ) from exc
    else:
        raise InvalidNumberError(
            f"Value must be a number: {value!r}"
        )

    if not math.isfinite(result):
        raise InvalidNumberError(
            f"Value must be a finite number: {value!r}"
        )

    return result



def is_positive(value: float) -> None:
    """Raise ValueError if value is not greater than zero.

    :param value: The numeric value to validate.
    :return: None.
    :raises ValueError: If the value is zero or negative.
    """
    if value <= 0:
        raise NonPositiveNumberError(
            f"Value must be a positive number: {value!r}"
        )
