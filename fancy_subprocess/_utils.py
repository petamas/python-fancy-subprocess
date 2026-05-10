__all__ = [
    'value_or',
]

from collections.abc import Sequence
from pathlib import Path
from typing import TypeVar

import oslex

T = TypeVar('T')
U = TypeVar('U')


def value_or(value: T | None, default: U) -> T | U:
    if value is None:
        return default
    else:
        return value


def oslex_join(cmd: Sequence[str | Path]) -> str:
    return oslex.join([str(arg) for arg in cmd])
