from abc import ABC, abstractmethod

class HasherServicePort(ABC):
    """Abstract password hashing operations."""

    @abstractmethod
    def hash_password(self, plain: str) -> str: ...

    @abstractmethod
    def verify_password(self, plain: str, hashed: str) -> bool: ...
