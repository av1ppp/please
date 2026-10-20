import typing
from pathlib import Path
from subprocess import CompletedProcess
from subprocess import run as subprocess_run
from sys import stderr, stdout

if typing.TYPE_CHECKING:
    from .types import Environment, PathLike


def shexec(
    args: list[PathLike] | PathLike,
    env: Environment | None = None,
    cwd: PathLike | None = None,
    timeout: float | None = None,
    input: bytes | None = None,
    capture_output: bool = False,
    shell: bool = True,
    check: bool = True,
) -> CompletedProcess[bytes]:
    return subprocess_run(
        check=check,
        input=input,
        timeout=timeout,
        args=_build_args(args),
        capture_output=capture_output,
        env=env,
        cwd=cwd,
        shell=shell,
        stdout=None if capture_output else stdout,
        stderr=None if capture_output else stderr,
    )


def _build_args(args: list[PathLike] | PathLike) -> str:
    if isinstance(args, str):
        return args
    if isinstance(args, Path):
        return str(args)
    return " ".join([str(v) for v in args])
