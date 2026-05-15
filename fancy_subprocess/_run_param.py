__all__ = [
    'ANY_EXIT_CODE',
    'AnyExitCode',
    'change_default_run_params',
    'check_run_params',
    'EnvOverrides',
    'force_run_params',
    'MaxOutputSize',
    'NO_LIMIT',
    'NoLimit',
    'RunParams',
    'Success',
]

from collections.abc import Mapping
from collections.abc import Sequence
from pathlib import Path
from typing import Optional
from typing import TypedDict

import typeguard
from typing_extensions import Unpack


class AnyExitCode:
    """
    Use an instance of this class (eg. fancy_subprocess.ANY_EXIT_CODE) as the 'success' argument to make run() and related functions treat any exit code as success.
    """

    pass


ANY_EXIT_CODE = AnyExitCode()

Success = Sequence[int] | AnyExitCode


class NoLimit:
    """
    Use an instance of this class (eg. fancy_subprocess.NO_LIMIT) as the 'max_output_size' argument to make run() and related functions not constrain the size of the output string.
    """

    pass


NO_LIMIT = NoLimit()

MaxOutputSize = int | NoLimit

EnvOverrides = Mapping[str, str]


class RunParams(TypedDict, total=False):
    message_quiet: Optional[bool]
    output_quiet: Optional[bool]
    description: Optional[str]
    success: Optional[Success]
    flush_before_subprocess: Optional[bool]
    trim_output_lines: Optional[bool]
    max_output_size: Optional[MaxOutputSize]
    retry: Optional[int]
    retry_initial_sleep_seconds: Optional[float]
    retry_backoff: Optional[float]
    env_overrides: Optional[EnvOverrides]
    cwd: Optional[str | Path]
    encoding: Optional[str]
    errors: Optional[str]
    replace_fffd_with_question_mark: Optional[bool]


def check_run_params(**kwargs: Unpack[RunParams]) -> None:
    try:
        typeguard.check_type(kwargs, RunParams, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS)
    except typeguard.TypeCheckError as e:
        # we don't wanna expose the stacktrace from typeguard to be able to replace it with another library if needed
        raise ValueError(str(e)) from None


def change_default_run_params(params: RunParams, **new_defaults: Unpack[RunParams]) -> None:
    check_run_params(**params)
    check_run_params(**new_defaults)

    for key in new_defaults.keys():
        if params.get(key) is None:
            # It's safe to ignore the TypedDict-related checks here because of the check_run_params() calls
            params[key] = new_defaults[key]  # type: ignore[literal-required] # ty: ignore[invalid-key]


def force_run_params(params: RunParams, **forced_values: Unpack[RunParams]) -> None:
    check_run_params(**params)
    check_run_params(**forced_values)

    for key in forced_values.keys():
        if key in params:
            raise ValueError(f'Trying to override forced keyword parameter {key} is disallowed')
        else:
            # It's safe to ignore the TypedDict-related checks here because of the check_run_params() calls
            params[key] = forced_values[key]  # type: ignore[literal-required] # ty: ignore[invalid-key]
