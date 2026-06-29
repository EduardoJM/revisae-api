from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.interfaces.paginator_port import Page, PaginatorPort
from domain.entities.notification import Notification
from domain.repositories.notification_port import NotificationPort
from infrastructure.database.models import NotificationModel
from infrastructure.mappers.notification import NotificationMapper


class NotificationRepository(NotificationPort):
    def __init__(
        self,
        session: AsyncSession,
        paginator: PaginatorPort,
    ) -> None:
        self._session = session
        self._paginator = paginator

    async def find_by_user_paginated(
        self,
        user_id: UUID,
        offset: int = 0,
        limit: int = 10,
        search: str = ''
    ) -> Page[Notification]:
        query = select(NotificationModel).where(NotificationModel.user_id == user_id)
        if search:
            query = query.filter(NotificationModel.name.match(f"%{search}%"))
        query = query.order_by(NotificationModel.created_at.desc())

        data: Page[NotificationModel] = await self._paginator.paginate(query, offset, limit)
        
        return Page(
            results=[NotificationMapper.to_entity(row) for row in data.results],
            total=data.total,
            per_page=data.per_page,
        )
    
    async def find_by_id(self, notification_id: UUID) -> Notification | None:
        row = await self._session.get(NotificationModel, notification_id)
        return NotificationMapper.to_entity(row) if row else None
    
    async def save(self, notification: Notification) -> None:
        model = NotificationMapper.to_model(notification)
        await self._session.merge(model)
