__all__ = [
    'stringify_exit_code',
]

import sys
from typing import Optional

if sys.platform == 'win32':
    from ntstatus import NtStatus
    from ntstatus import NtStatusSeverity
    from ntstatus import ThirtyTwoBits
else:
    import signal

    def _signal_name(signal_value: int) -> Optional[str]:
        try:
            return signal.Signals(signal_value).name
        except ValueError:
            return None


def stringify_exit_code(exit_code: int) -> Optional[str]:
    if sys.platform == 'win32':
        # Windows
        if exit_code == 3:
            # abort() results in exit code 3: https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/abort
            # While exit code 3 does not necessarily mean aborted (because applications may use it as a generic error code),
            # it's common enough to be worth handling. "?" included to signal the uncertainty.
            return 'aborted?'

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
            return _signal_name(-exit_code) or 'unknown signal'
        elif exit_code == 126:
            return 'COULD_NOT_EXECUTE'
        elif exit_code == 127:
            return 'COMMAND_NOT_FOUND'
        elif exit_code in range(129, 160):
            return _signal_name(exit_code - 128) or 'unknown signal'

    return None
