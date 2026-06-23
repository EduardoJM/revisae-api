import re
from dataclasses import dataclass

_EMAIL_RE = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        if not _EMAIL_RE.match(self.value):
            raise ValueError(f"Invalid email format: '{self.value}'")
        # normalise to lowercase
        object.__setattr__(self, "value", self.value.lower())

    def __str__(self) -> str:
        return self.value
