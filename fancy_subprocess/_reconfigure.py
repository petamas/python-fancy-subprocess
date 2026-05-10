__all__ = [
    'reconfigure_standard_output_streams',
]

import io
import sys
from typing import Optional, TypedDict

from typing_extensions import Unpack


class ReconfigureParams(TypedDict, total=False):
    encoding: Optional[str]
    errors: Optional[str]
    newline: Optional[str]
    line_buffering: Optional[bool]
    write_through: Optional[bool]


def _reconfigure_standard_stream(stream: object, name: str, **kwargs: Unpack[ReconfigureParams]) -> None:
    if stream is None:
        raise TypeError(f'{name} is None')

    if not isinstance(stream, io.TextIOWrapper):
        raise TypeError(f'{name} is not a TextIOWrapper: {repr(stream)}')

    stream.reconfigure(**kwargs)


def reconfigure_standard_output_streams(**kwargs: Unpack[ReconfigureParams]) -> None:
    """
    Calls `sys.stdout.reconfigure()` and `sys.stderr.reconfigure()` with the provided parameters. Raises `TypeError` if either `sys.stdout` or `sys.stderr` is not an instance of `io.TextIOWrapper`.
    """

    _reconfigure_standard_stream(sys.stdout, 'sys.stdout', **kwargs)
    _reconfigure_standard_stream(sys.stderr, 'sys.stderr', **kwargs)
