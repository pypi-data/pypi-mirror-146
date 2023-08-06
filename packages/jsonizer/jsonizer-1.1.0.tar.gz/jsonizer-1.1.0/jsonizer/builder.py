import inspect
import itertools
from typing import Type, Generator

from jsonizer.hashes import hash_arguments
from jsonizer.types import Argument, Arguments


class Builder:

    def __init__(self, class_type: Type):
        self.class_type = class_type

    def build(self) -> list[int]:
        constructor = inspect.signature(self.class_type.__init__)
        required, optionals = self.split_arguments(constructor)
        hashes = self.calculate_hashes(required, optionals)
        return list(hashes)

    def split_arguments(self, signature: inspect.Signature) -> (Arguments, Arguments):
        required = list()
        optional = list()
        for (i, parameter) in enumerate(signature.parameters.values()):
            if i == 0 or self._is_variadic(parameter):  # skip self, *args, **kwargs
                continue
            default = parameter.default
            if default is inspect.Parameter.empty:
                argument = Argument(parameter.name, has_default=False)
                required.append(argument)
            else:
                argument = Argument(parameter.name, has_default=True, default=default)
                optional.append(argument)
        return required, optional

    @staticmethod
    def calculate_hashes(required: Arguments, optionals: Arguments) -> Generator[int, None, None]:
        for count in range(len(optionals) + 1):
            for optionals_current in itertools.combinations(optionals, count):
                arguments = required + list(optionals_current)
                yield hash_arguments(arguments)

    @staticmethod
    def _is_variadic(parameter: inspect.Parameter) -> bool:
        """Variadic parameters is *args and **kwargs"""
        return parameter.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
