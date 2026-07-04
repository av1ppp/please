from dataclasses import dataclass


@dataclass()
class Argument:
    key: str | None
    value: str


def parse_args(args: list[str]) -> list[Argument]:
    result: list[Argument] = []

    for arg in args:
        if arg.startswith("-"):
            parts = arg[1:].split("=", 2)
            if len(parts) == 1:
                value = ""
            else:
                value = parts[1]
            arg_ = Argument(key=parts[0], value=value)
        else:
            arg_ = Argument(key=None, value=arg)

        result.append(arg_)

    return result
