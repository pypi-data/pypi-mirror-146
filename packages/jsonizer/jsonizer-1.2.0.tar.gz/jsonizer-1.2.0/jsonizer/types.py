from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Argument:
    name: str
    has_default: bool
    default: Any = None


Arguments = list[Argument]
