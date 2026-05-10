__all__ = [
    'checked_which',
    'RunProcessError',
    'RunProcessResult',
    'SILENCE',
    'which',
]

from pathext import checked_which
from pathext import which

from fancy_subprocess._run_core import RunError
from fancy_subprocess._run_core import RunResult

RunProcessError = RunError
RunProcessResult = RunResult


def SILENCE(msg: str) -> None:
    """
    Helper function that takes a string, and does nothing with it. Meant to be passed as the print_message or print_output argument of run() and related functions to silence the corresponding output stream.
    """

    pass
