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
