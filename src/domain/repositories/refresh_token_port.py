from abc import ABC, abstractmethod
from uuid import UUID

class RefreshTokenPort(ABC):
    @abstractmethod
    async def save(self, user_id: UUID, token_hash: str, expires_at: object) -> None: ...

    @abstractmethod
    async def find(self, token_hash: str) -> dict | None: ...

    @abstractmethod
    async def revoke(self, token_hash: str) -> None: ...

    @abstractmethod
    async def revoke_all_for_user(self, user_id: UUID) -> None: ...
