# jsonizer

It is a library for parsing nested JSONs into predefined classes 🔨✨

In many cases you can use [dataclasses](https://docs.python.org/3/library/dataclasses.html)
or [pydantic](https://pypi.org/project/pydantic) for parsing JSON into Python classes.
But sometimes you need to parse JSON into some predefined classes.
You can't change this classes, or it is too time-consuming.
For example, this classes can be imported from another library.
In this case, this is an ideal solution for you :)

## Reasons to use jsonizer

- Supports nested classes
- Fastest class detection
- No dependencies

## Installation

```bash
pip install jsonizer
```

## Usage sample

```python
from jsonizer import Jsonizer

class Egg:
    def __init__(self, size, color='white'):
        self._size = size
        self._color = color
    def __repr__(self):
        return f'{self._color} egg with size {self._size}'

class Bird:
    def __init__(self, name, eggs):
        self._name = name
        self._eggs = eggs
    def __repr__(self):
        return f'Bird "{self._name}" with eggs {self._eggs}'

json_data = {
    'name': 'Duck',
    'eggs': [{
        'size': 12,
    }, {
        'size': 69,
        'color': 'purple',
    }]
}
parser = Jsonizer(Bird, Egg)
bird = parser.parse(json_data)
print(bird)
# >>> Bird "Duck" with eggs [white egg with size 12, purple egg with size 69]
```

This sample can be found [here](examples/example_nohints.py).
For simplicity, there are no type hints (and no PEP8 style).
But **jsonizer** allows and insists on using type hints.
[Here](examples/example_hints.py) is same sample but with type hints

## Parsing initial arguments

Class `Jsonizer` require the list of classes in that JSONs can be parsed as first argument,
they can be in any order
<details>
<summary>Optional arguments</summary>

| Name               | Type   | Default | Description                                                                                    |
|--------------------|--------|---------|------------------------------------------------------------------------------------------------|
| `ignore_ambiguity` | `bool` | `False` | Ignore exceptions when dicts can be matched to two or more constructors (see exceptions block) |
| `disallow_dicts`   | `bool` | `False` | Disallow to have dict as class argument (see exceptions block)                                 |
| `lowercase_keys`   | `bool` | `False` | Lowercase all keys (names) in input JSON                                                       |
| `replace_space`    | `str`  | `None`  | If not `None`, replace space in keys (names) in input JSON with this value                     |

</details>

## Parsing functions

| Function            | Description                     | Sample                       |
|---------------------|---------------------------------|------------------------------|
| `parse(dict/list)`  | Parse object of list of objects | `parse({'name': 'Alice'})`   |
| `parse_string(str)` | Parse JSON string               | `parse('{"name": "Alice"}')` |
| `parse_file(str)`   | Parse JSON file by filename     | `parse('sample.json')`       |

## Exceptions

There are 3+1 kind of exceptions:

<details>
<summary>1. AmbiguityParamsException</summary>

It appears when **jsonizer** two classes can have common init params.
In example below, json data `{"name": "Alice"}` can be matched to both classes.
You can ignore such situations by passing `ignore_ambiguity=True` to parser

```python
class Person:
    def __init__(self, name: str):
        # .. some logic ...
class Worker:
    def __init__(self, name: str, income: int = 0):
        # .. some logic ...

parser = Jsonizer(Worker, Person)
# >>> jsonizer.exceptions.AmbiguityParamsException: Some signatures can be matched to class "<class 'sample.Worker'>" and "<class 'sample.Person'>" simultaneously

parser = Jsonizer(Worker, Person, ignore_ambiguity=True)
parser.parse(...)
```

</details>

<details>
<summary>2. UnparsedJsonException</summary>

In some _rarely cases_ (I really don't know why) you may want to not have dicts as arguments.
You can reach this by passing `disallow_dicts=True` to parser

```python
class Person:
    def __init__(self, name: str, contacts: Any):
        # .. some logic ...

person_data = {'name': 'Alice', 'contacts': {'phone': '123-456-7890'}}

parser = Jsonizer(Person, disallow_dicts=True)
parser.parse(person_data)
# >>> jsonizer.exceptions.UnparsedJsonException: Cannot recognize class for JSON data "{'phone': '123-456-7890'}"

parser = Jsonizer(Person)
person = parser.parse(person_data)
# >> Hi! I am Alice, my contacts are {'phone': '123-456-7890'}
```

</details>

<details>
<summary>3. FullyUnparsedException</summary>

Cannot parse main dict (root/first elements) into one of passed classes.
Check keys of JSON data, is they really matched to any class

</details>

<details>
<summary>4. JSONDecodeError (standard Python exception)</summary>

Default Python exception in case of invalid JSON file or string.
Check your JSON, 99.69% that it is invalid. You can check it [here](https://jsonformatter.curiousconcept.com).
See more in [documentation](https://docs.python.org/3/library/json.html#json.JSONDecodeError)

PS in JSON you must use double quotes `"` instead of single `'`, and `null` instead of `None`

</details>

## FAQ

**Q: Why is it so fast?**

A: It uses hashes to represent all possible constructor (regardless the arguments order)

**Q: What does parser do with `self`, `*args` and `**kwargs`?**

A: It skips them, even if they have different name

**Q: Where there are so few tests?**

A: They are waiting while you will code them :)

## More

PyPI: https://pypi.org/project/jsonizer

Repository: https://github.com/abionics/jsonizer

Developer: Alex Ermolaev (Abionics)

Email: abionics.dev@gmail.com

License: MIT (see LICENSE.txt)
