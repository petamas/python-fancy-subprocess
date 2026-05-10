__all__ = [
    'value_or',
]

import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Optional
from typing import TypeVar

import oslex

if sys.platform == 'win32':
    from ntstatus import NtStatus
    from ntstatus import NtStatusSeverity
    from ntstatus import ThirtyTwoBits
else:
    import signal

T = TypeVar('T')
U = TypeVar('U')


def value_or(value: T | None, default: U) -> T | U:
    if value is None:
        return default
    else:
        return value


def oslex_join(cmd: Sequence[str | Path]) -> str:
    return oslex.join([str(arg) for arg in cmd])


def stringify_exit_code(exit_code: int) -> Optional[str]:
    if sys.platform == 'win32':
        # Windows
        if not ThirtyTwoBits.check(exit_code):
            return None

        try:
            status = NtStatus.decode(exit_code)
            if NtStatus.severity(status) != NtStatusSeverity.STATUS_SEVERITY_SUCCESS:
                return status.name
        except ValueError:
            pass

        return f'0x{ThirtyTwoBits(exit_code).unsigned_value:08X}'
    else:
        # POSIX
        if exit_code < 0:
            try:
                return signal.Signals(-exit_code).name
            except ValueError:
                return 'unknown signal'

    return None
