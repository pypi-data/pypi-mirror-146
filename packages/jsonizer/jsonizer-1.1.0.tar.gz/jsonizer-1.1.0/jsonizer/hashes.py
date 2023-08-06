from typing import Iterable

from jsonizer.types import Arguments


def hash_arguments(arguments: Arguments) -> int:
    names = tuple(argument.name for argument in arguments)
    return hash_names(names)


def hash_names(names: Iterable[str]) -> int:
    names_sorted = tuple(sorted(names))
    return hash(names_sorted)
