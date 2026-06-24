import re
from dataclasses import dataclass


_COLOR_RE = re.compile(r'#?[0-9abcdef]{8}|#?[0-9abcdef]{6}|#?[0-9abcdef]{4}|#?[0-9abcdef]{3}')

@dataclass(frozen=True)
class HexColor:
    value: str

    def __post_init__(self) -> None:
        if not _COLOR_RE.match(self.value.lower()):
            raise ValueError(f"Invalid color format: '{self.value}'")
        # normalise to lowercase
        object.__setattr__(self, "value", self.value.lower())

    def __str__(self) -> str:
        return self.value
