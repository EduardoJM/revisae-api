from uuid import UUID
from datetime import datetime
from abc import ABC, abstractmethod

class JWTServicePort(ABC):
    """Abstract JWT operations."""

    @abstractmethod
    def create_access_token(self, user_id: UUID) -> str: ...

    @abstractmethod
    def create_refresh_token(self, user_id: UUID) -> tuple[str, str, datetime]:
        """Returns (raw_token, token_hash, expires_at)."""
        ...

    @abstractmethod
    def decode_token(self, token: str) -> dict: ...
