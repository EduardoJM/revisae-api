from dataclasses import dataclass

@dataclass(frozen=True)
class HashedPassword:
    """Stores an already-hashed password string. Hashing lives in the adapter layer."""
    value: str

    def __str__(self) -> str:
        return self.value
