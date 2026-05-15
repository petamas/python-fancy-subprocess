import pickle
from collections.abc import Iterator
from contextlib import contextmanager

import pytest

from fancy_subprocess import RunError
from fancy_subprocess import RunResult


def test_runerror_picklable() -> None:
    """
    There are certain exceptions that cannot be pickled, see:
    - https://github.com/python/cpython/issues/101159 (original issue with long discussion)
    - https://github.com/python/cpython/issues/44791 (closed issue linking various related issues)
    - https://github.com/python/cpython/issues/87626 (open issue that actually matches ours)
    RunError's previous implementation (using @dataclass(kw_only=True)) was like that.
    This test guards against the class becoming unpicklable again.
    """
    original_error = RunError(['notepad.exe'], RunResult(exit_code=0))
    pickled_error = pickle.loads(pickle.dumps(original_error))
    assert original_error.cmd == pickled_error.cmd
    assert original_error.result == pickled_error.result


def test_runerror_is_contextlib_contextmanager_compatible() -> None:
    """
    On Python 3.11+, RunError's previous implementation (using @dataclass(frozen=True)) caused contextmanager() to raise an exception:
    > dataclasses.FrozenInstanceError: cannot assign to field '__traceback__'
    """

    @contextmanager
    def manager() -> Iterator[int]:
        yield 3

    with pytest.raises(RunError):
        with manager() as exit_code:
            raise RunError(['notepad.exe'], RunResult(exit_code=exit_code))
