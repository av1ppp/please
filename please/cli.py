from pathlib import Path
from sys import argv

from .internal.taskcontext import TaskContext
from .internal.tasks import tasks

init_command = ["-i", "-init", "--init"]
help_command = ["-h", "-help", "--help"]
version_command = ["-v", "-version", "--version"]

help_indent = "    "


def main():
    load_pleasefile_if_exists()

    args = argv[1:]

    if len(args) == 0 or args[0] in help_command:
        print_help()
        return

    if args[0] in init_command:
        init_pleasefile()
        return

    if args[0] in version_command:
        print_version()
        return

    if args[0] in tasks:
        task = tasks[args[0]]
        ctx = TaskContext()
        task(ctx)
        return

    print(f"ERROR: Command or task '{args[0]}' not found. Try to use -h command.")


def init_pleasefile():
    raise NotImplementedError()


def print_version():
    raise NotImplementedError()


def print_help():
    print("COMMANDS:")
    print_command(init_command, "Create empty Pleasefile")
    print_command(help_command, "Show this message")
    print_command(version_command, "Show version")

    if len(tasks) > 0:
        print()
        print("TASKS:")
        for task_name, _ in tasks.items():
            print(f"{help_indent}{task_name}")


def load_pleasefile_if_exists():
    filenames = [
        Path("Pleasefile.py"),
        Path("Pleasefile"),
    ]

    for filename in filenames:
        if not filename.exists():
            continue

        with open(filename, mode="r") as file:
            data = file.read()
            exec(data)
            return


def print_command(command: list, description: str):
    print(help_indent + ", ".join(command).ljust(26, " ") + description)


if __name__ == "__main__":
    main()
