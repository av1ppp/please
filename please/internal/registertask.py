import typing

from .tasks import tasks

if typing.TYPE_CHECKING:
    from .taskfunc import TaskFunc


def register_task(name: str | None = None) -> typing.Callable[[TaskFunc], TaskFunc]:
    def decorator(func: TaskFunc) -> TaskFunc:
        nonlocal name

        if name is None:
            name = func.__name__

        if name in tasks:
            raise Exception(f"Task {name} already registered")

        tasks[name] = func

        # def wrapper() -> None:
        #     context = TaskContext()
        #     return func(context)

        # return wrapper
        return func

    return decorator
