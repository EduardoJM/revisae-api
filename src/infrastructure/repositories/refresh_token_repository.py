from uuid import UUID
from datetime import datetime, UTC

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from domain.repositories.refresh_token_port import RefreshTokenPort
from infrastructure.database.models.refresh_token import RefreshTokenModel

class RefreshTokenRepository(RefreshTokenPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, user_id: UUID, token_hash: str, expires_at: datetime) -> None:
        model = RefreshTokenModel(
            token_hash=token_hash,
            user_id=user_id,
            expires_at=expires_at,
        )
        self._session.add(model)

    async def find(self, token_hash: str) -> dict | None:
        row = await self._session.get(RefreshTokenModel, token_hash)
        if not row:
            return None
        if row.expires_at.replace(tzinfo=UTC) < datetime.now(UTC):
            await self._session.delete(row)
            return None
        return {"user_id": str(row.user_id), "expires_at": row.expires_at}

    async def revoke(self, token_hash: str) -> None:
        row = await self._session.get(RefreshTokenModel, token_hash)
        if row:
            await self._session.delete(row)

    async def revoke_all_for_user(self, user_id: UUID) -> None:
        await self._session.execute(
            delete(RefreshTokenModel).where(RefreshTokenModel.user_id == user_id)
        )
