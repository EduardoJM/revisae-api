from uuid import UUID
from abc import ABC, abstractmethod

from domain.entities.user import User

class UserRepositoryPort(ABC):
    @abstractmethod
    async def find_by_id(self, user_id: UUID) -> User | None: ...

    @abstractmethod
    async def find_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def save(self, user: User) -> None: ...
