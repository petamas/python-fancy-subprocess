__all__ = [
    'run_silenced',
    'run_indented',
]

from collections.abc import Sequence
from pathlib import Path
from typing import Optional

from typing_extensions import Unpack

from fancy_subprocess._print import Indent
from fancy_subprocess._print import PrintFunction
from fancy_subprocess._print import indented_print_factory
from fancy_subprocess._print import silenced_print
from fancy_subprocess._run_core import RunResult
from fancy_subprocess._run_core import run
from fancy_subprocess._run_param import RunParams
from fancy_subprocess._run_param import check_run_params
from fancy_subprocess._run_param import force_run_params
from fancy_subprocess._utils import oslex_join


def run_silenced(
    cmd: Sequence[str | Path],
    *,
    print_message: Optional[PrintFunction] = None,
    **kwargs: Unpack[RunParams],
) -> RunResult:
    """
    Specialized version of `fancy_subprocess.run()`, primarily used to run a command and later process its output.

    Differences compared to `fancy_subprocess.run()`:
    - `output_quiet` cannot be set from the calling side, it is always set to `True`. Note that this affects `description`'s default value.
    - `print_output` cannot be set from the calling side (because it wouldn't matter anyway because of `output_quiet=True`).

    All other `fancy_subprocess.run()` arguments are available and behave the same.
    """

    check_run_params(**kwargs)

    forwarded_args = kwargs.copy()
    force_run_params(forwarded_args, output_quiet=True)

    return run(
        cmd,
        print_message=print_message,
        print_output=silenced_print,
        **forwarded_args,
    )


def run_indented(
    cmd: Sequence[str | Path],
    *,
    print_message: Optional[PrintFunction] = None,
    indent: Optional[Indent] = None,
    **kwargs: Unpack[RunParams],
) -> RunResult:
    """
    Specialized version of `fancy_subprocess.run()` which prints the command's output indented by a user-defined amount.

    The `print_output` argument is replaced by `indent`, which can be set to either the number of spaces to use for indentation or any custom indentation string (eg. `\t`).

    All other `fancy_subprocess.run()` arguments are available and behave the same.
    """

    check_run_params(**kwargs)

    return run(
        cmd,
        print_message=print_message,
        print_output=indented_print_factory(indent),
        **kwargs,
    )
