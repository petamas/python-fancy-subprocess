__all__ = [
    'value_or',
]

from typing import TypeVar

T = TypeVar('T')
U = TypeVar('U')


def value_or(value: T | None, default: U) -> T | U:
    if value is None:
        return default
    else:
        return value
