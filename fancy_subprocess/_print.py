__all__ = [
    'default_print',
    'error_print',
    'Indent',
    'indented_print',
    'indented_print_factory',
    'PrintFunction',
    'silenced_print',
]

import sys
from collections.abc import Callable
from typing import Optional

PrintFunction = Callable[[str], None]

Indent = int | str


def silenced_print(line: str) -> None:
    pass


def indented_print(line: str, indent: Optional[Indent] = None) -> None:
    if indent is None:
        real_indent = 4 * ' '
    elif isinstance(indent, int):
        real_indent = indent * ' '
    else:
        real_indent = indent

    print(f'{real_indent}{line}', flush=True)


def indented_print_factory(indent: Optional[Indent] = None) -> PrintFunction:
    return lambda line: indented_print(line, indent)


def default_print(line: str) -> None:
    indented_print(line, indent='')


def error_print(line: str) -> None:
    print(line, file=sys.stderr, flush=True)
