import typing

from .taskcontext import TaskContext

TaskFunc = typing.Callable[[TaskContext], None]
