from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.user import User
from domain.repositories.user_port import UserPort
from infrastructure.database.models import UserModel
from infrastructure.mappers.user import UserMapper

class UserRepository(UserPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_id(self, user_id: UUID) -> User | None:
        row = await self._session.get(UserModel, user_id)
        return UserMapper.to_entity(row) if row else None

    async def find_by_email(self, email: str) -> User | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        row = result.scalar_one_or_none()
        return UserMapper.to_entity(row) if row else None

    async def save(self, user: User) -> None:
        model = UserMapper.to_model(user)
        await self._session.merge(model)
