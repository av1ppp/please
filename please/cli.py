import importlib
import sys
import typing
from pathlib import Path
from sys import argv, exit

sys.path.append("./")

from importlib.metadata import version

from .internal.taskcontext import TaskContext

if typing.TYPE_CHECKING:
    from .internal.taskfunc import TaskFunc

ver = version("please_av1ppp")

pleasefile_module = "Pleasefile"
pleasefile_name = Path(pleasefile_module + ".py")


init_command = ["-i", "-init"]
help_command = ["-h", "-help"]
version_command = ["-v", "-version"]

help_indent = "    "


def main() -> None:
    tasks = get_tasks_from_pleasefile()
    args = argv[1:]

    if len(args) == 0 or args[0] in help_command:
        print_help(tasks)
        return

    if args[0] in init_command:
        init_pleasefile()
        return

    if args[0] in version_command:
        print_version()
        return

    if tasks is not None and args[0] in tasks:
        task = tasks[args[0]]
        ctx = TaskContext(args[1:])
        task(ctx)
        return

    panic(f"Command or task '{args[0]}' not found. Try to use -h command.")


def init_pleasefile() -> None:
    if pleasefile_name.exists():
        panic("Pleasefile already created")

    with open(pleasefile_name, mode="w") as file:
        file.write(
            """import please


@please.task()
def start(ctx: please.TaskContext):
    mode = ctx.string("mode") or "prod"
    print(f"*starting app in {mode} mode*")
"""
        )


def print_version() -> None:
    print("Please v" + ver)


def print_help(tasks: dict[str, TaskFunc] | None) -> None:
    print("PLEASE - simple task runner.")
    print()

    print("COMMANDS:")
    print_command(init_command, "Create empty Pleasefile")
    print_command(help_command, "Show this message")
    print_command(version_command, "Show version")

    if tasks is not None and len(tasks) > 0:
        print()
        print("TASKS:")
        for task_name, _ in tasks.items():
            print(f"{help_indent}{task_name}")


def get_tasks_from_pleasefile() -> dict[str, TaskFunc] | None:
    try:
        module = importlib.import_module(pleasefile_module)
    except ModuleNotFoundError:
        return None

    try:
        tasks: dict[str, TaskFunc] = module.please.internal.tasks.tasks
    except AttributeError:
        return None

    return tasks


def print_command(command: list[str], description: str) -> None:
    print(help_indent + ", ".join(command).ljust(26, " ") + description)


def panic(*values: object) -> None:
    print("ERROR:", *values)
    exit(1)


if __name__ == "__main__":
    main()
