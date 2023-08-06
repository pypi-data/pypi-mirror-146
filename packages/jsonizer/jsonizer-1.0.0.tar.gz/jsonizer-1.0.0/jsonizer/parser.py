import json
from typing import Type, Any

from jsonizer.builder import Builder
from jsonizer.exceptions import AmbiguityParamsException, UnparsedJsonException
from jsonizer.hashes import hash_names


class Parser:

    def __init__(
            self,
            *classes: Type,
            ignore_ambiguity: bool = False,
            disallow_dicts: bool = False,
            lowercase_keys: bool = False,
            replace_space: str = None,
    ):
        """
        :param classes: Variadic list of classes in that JSONs can be parsed (in any order)
        :param ignore_ambiguity: Ignore exceptions when dicts can be matched to two or more constructors
        :param disallow_dicts: Disallow to have dict as class argument
        :param lowercase_keys: Lowercase all keys (names) in input JSON
        :param replace_space: If not `None`, replace space in keys (names) in input JSON with this value
        """
        self._ignore_ambiguity = ignore_ambiguity
        self._disallow_dicts = disallow_dicts
        self._lowercase_keys = lowercase_keys
        self._replace_space = replace_space
        self._hashes = self._create_hashes(classes)

    def _create_hashes(self, classes: tuple[Type]) -> dict[int, Type]:
        hashes = dict()
        for class_type in classes:
            class_hashes = self._calculate_hashes(class_type)
            if not self._ignore_ambiguity:
                self._check_ambiguity(hashes, class_hashes)
            hashes.update(class_hashes)
        return hashes

    @staticmethod
    def _check_ambiguity(hashes_1: dict[int, Type], hashes_2: dict[int, Type]):
        duplicates = hashes_1.keys() & hashes_2.keys()
        if len(duplicates) > 0:
            duplicate = duplicates.pop()
            raise AmbiguityParamsException(hashes_1[duplicate], hashes_2[duplicate])

    @staticmethod
    def _calculate_hashes(class_type: Type) -> dict[int, Type]:
        builder = Builder(class_type)
        hashes = builder.build()
        return dict.fromkeys(hashes, class_type)

    def parse_string(self, string: str) -> Any:
        """
        :param string: JSON string
        :return: parsed class (or list of classes)
        """
        data = json.loads(string)
        return self.parse(data)

    def parse_file(self, filename: str) -> Any:
        """
        :param filename: name of file with JSON
        :return: parsed class (or list of classes)
        """
        with open(filename, 'r') as file:
            data = json.load(file)
        return self.parse(data)

    def parse(self, data: dict | list[dict]) -> Any:
        """
        :param data: data (dict or list) to parse
        :return: parsed class (or list of classes)
        """
        if isinstance(data, list):
            return self._parse_list(data)
        else:
            return self._parse_dict(data)

    def _parse_list(self, data: list[dict]) -> list[Any]:
        return [
            self._parse_dict(sub_data)
            for sub_data in data
        ]

    def _parse_dict(self, data: dict) -> Any:
        hash_ = hash_names(data.keys())
        type_class = self._hashes.get(hash_)
        if type_class is None:
            if self._disallow_dicts:
                raise UnparsedJsonException(data)
            return data
        init_params = dict()
        for key, value in data.items():
            key = self._format_key(key)
            init_params[key] = self._parse_value(value)
        return type_class(**init_params)

    def _format_key(self, key: str) -> str:
        if self._lowercase_keys:
            key = key.lower()
        if self._replace_space is not None:
            key = key.replace(' ', self._replace_space)
        return key

    def _parse_value(self, value: Any) -> Any:
        if isinstance(value, dict):
            return self._parse_dict(value)
        elif isinstance(value, list):
            only_dicts = self._is_only(value, dict)
            only_lists = self._is_only(value, list)
            if only_dicts or only_lists:
                return self._parse_list(value)
        return value

    @staticmethod
    def _is_only(array: list, subtype: Type) -> bool:
        return all(isinstance(element, subtype) for element in array)
