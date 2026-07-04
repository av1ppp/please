import typing

if typing.TYPE_CHECKING:
    from .taskfunc import TaskFunc

tasks: dict[str, TaskFunc] = {}
