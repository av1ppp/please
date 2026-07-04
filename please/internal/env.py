import typing
from os import environ

if typing.TYPE_CHECKING:
    from .types import Environment, PathLike


def parseenv(path: PathLike) -> Environment:
    with open(path, "r") as file:
        lines = file.readlines()

    env: Environment = dict()

    for line in lines:
        line = line.strip()
        if len(line) == 0 or line.startswith("#"):
            continue

        split_line = line.split("=", 1)
        if len(split_line) != 2:
            raise Exception("invalid line: " + line)

        key = split_line[0].strip()

        value = split_line[1].strip()
        if "#" in value:
            value = value.split("#")[0]
        value = value.strip()

        if value.startswith('"') and value.endswith('"'):
            value = value.strip('"')

        if value.startswith("'") and value.endswith("'"):
            value = value.strip("'")

        env[key] = value

    return env


def loadenv(path: PathLike) -> None:
    env = parseenv(path)
    for key, value in env.items():
        environ[key] = value
