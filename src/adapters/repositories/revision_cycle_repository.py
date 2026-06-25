from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from application.interfaces.paginator_port import Page, PaginatorPort
from domain.entities.revision_cycle import RevisionCycle
from domain.repositories.revision_cycle_port import RevisionCyclePort
from infrastructure.database.models import RevisionCycleModel
from infrastructure.mappers.revision_cycle import RevisionCycleMapper

class RevisionCycleRepository(RevisionCyclePort):
    def __init__(
        self,
        session: AsyncSession,
        paginator: PaginatorPort,
    ) -> None:
        self._session = session
        self._paginator = paginator

    async def find_by_id(self, revision_cycle_id: UUID) -> RevisionCycle | None:
        row = await self._session.get(RevisionCycleModel, revision_cycle_id)
        return RevisionCycleMapper.to_entity(row) if row else None

    async def find_by_user_paginated(
        self,
        user_id: UUID,
        offset: int = 0,
        limit: int = 10,
        search: str = ''
    ) -> Page[RevisionCycle]:
        query = select(RevisionCycleModel).where(RevisionCycleModel.user_id == user_id)
        if search:
            query = query.filter(RevisionCycleModel.name.match(f"%{search}%"))
        query = query.order_by(RevisionCycleModel.created_at.desc())

        data: Page[RevisionCycleModel] = await self._paginator.paginate(query, offset, limit)

        return Page(
            results=[RevisionCycleMapper.to_entity(row) for row in data.results],
            total=data.total,
            per_page=data.per_page,
        )

    async def delete(self, revision_cycle_id):
        await self._session.execute(
            delete(RevisionCycleModel).where(RevisionCycleModel.id == revision_cycle_id)
        )

    async def save(self, revision_cycle: RevisionCycle) -> None:
        model = RevisionCycleMapper.to_model(revision_cycle)
        await self._session.merge(model)
