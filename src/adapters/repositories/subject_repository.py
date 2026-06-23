from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.interfaces.paginator_port import Page, PaginatorPort
from domain.entities.subject import Subject
from domain.repositories.subject_port import SubjectPort
from infrastructure.database.models import SubjectModel
from infrastructure.mappers.subject import SubjectMapper

class SubjectRepository(SubjectPort):
    def __init__(
        self,
        session: AsyncSession,
        paginator: PaginatorPort,
    ) -> None:
        self._session = session
        self._paginator = paginator
    
    async def find_by_id(self, subject_id: UUID) -> Subject | None:
        row = await self._session.get(SubjectModel, subject_id)
        return SubjectMapper.to_entity(row) if row else None

    async def find_by_user_paginated(
        self,
        user_id: UUID,
        offset: int = 0,
        limit: int = 10,
        search: str = ''
    ) -> Page[Subject]:
        query = select(SubjectModel).where(SubjectModel.user_id == user_id)
        if search:
            query = query.filter(SubjectModel.name.match(f"%{search}%"))
        query = query.order_by(SubjectModel.created_at.desc())

        data: Page[SubjectModel] = await self._paginator.paginate(query, offset, limit)
        
        return Page(
            results=[SubjectMapper.to_entity(row) for row in data.results],
            total=data.total,
        )
    
    async def delete(self, subject_id):
        raise Exception("A")

    async def save(self, subject: Subject) -> None:
        model = SubjectMapper.to_model(subject)
        await self._session.merge(model)
