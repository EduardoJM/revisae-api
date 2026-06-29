from uuid import UUID
from abc import ABC, abstractmethod

from domain.entities.notification import Notification
from application.interfaces.paginator_port import Page

class NotificationPort(ABC):
    @abstractmethod
    async def find_by_id(self, notification_id: UUID) -> Notification | None: ...

    @abstractmethod
    async def find_by_user_paginated(
        self,
        user_id: UUID,
        offset: int = 0,
        limit: int = 10,
        search: str = ''
    ) -> Page[Notification]: ...

    @abstractmethod
    async def save(self, notification: Notification) -> None: ...
