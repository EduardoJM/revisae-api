from uuid import UUID, uuid4

from domain.entities.notification import Notification
from domain.repositories.notification_port import NotificationPort
from domain.exceptions.notification import NotificationNotFound
from application.schemas.notification import (
    NotificationOutput, PaginatedNotificationOutput
)

def _notification_to_output(notification: Notification) -> NotificationOutput:
    return NotificationOutput(
        id=notification.id,
        title=notification.title,
        description=notification.description,
        is_readed=notification.is_readed,
        created_at=notification.created_at
    )

class ListNotifications:
    def __init__(self, notification_repo: NotificationPort) -> None:
        self._notifications = notification_repo

    async def execute(
        self,
        user_id: UUID,
        offset: int = 0,
        limit: int = 10,
        search: str = '',
    ) -> PaginatedNotificationOutput:
        data = await self._notifications.find_by_user_paginated(user_id, offset, limit, search)

        return PaginatedNotificationOutput(
            results=[_notification_to_output(notification) for notification in data.results],
            total=data.total,
            per_page=data.per_page,
        )

class GetNotification:
    def __init__(self, notification_repo: NotificationPort) -> None:
        self._notifications = notification_repo

    async def execute(self, user_id: UUID, notification_id: UUID) -> NotificationOutput:
        notification = await self._notifications.find_by_id(notification_id)
        if not notification:
            raise NotificationNotFound(notification_id)
        if not notification.belongs_to(user_id):
            raise NotificationNotFound(notification_id)
        return _notification_to_output(notification)

class MarkNotificationAsReaded:
    def __init__(self, notification_repo: NotificationPort) -> None:
        self._notifications = notification_repo

    async def execute(self, user_id: UUID, notification_id: UUID) -> NotificationOutput:
        notification = await self._notifications.find_by_id(notification_id)
        if not notification:
            raise NotificationNotFound(notification_id)
        if not notification.belongs_to(user_id):
            raise NotificationNotFound(notification_id)
        notification.mark_as_readed()

        await self._notifications.save(notification)

        return _notification_to_output(notification)
