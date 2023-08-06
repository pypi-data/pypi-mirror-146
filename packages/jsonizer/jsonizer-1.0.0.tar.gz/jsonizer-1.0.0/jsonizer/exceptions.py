from typing import Type


class JsonizerException(Exception):
    pass


class AmbiguityParamsException(JsonizerException):
    def __init__(self, class_1: Type, class_2: Type):
        super().__init__(
            f'Some signatures can be matched to class "{class_1}" and "{class_2}" simultaneously\n'
            'Hint: try to pass `ignore_ambiguity=True` to parser'
        )


class UnparsedJsonException(JsonizerException):
    def __init__(self, data: dict):
        super().__init__(
            f'Cannot recognize class for JSON data "{data}"\n'
            'Hint: try to pass `disallow_dicts=False` to parser'
        )
