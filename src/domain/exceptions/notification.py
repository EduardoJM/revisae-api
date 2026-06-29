from uuid import UUID

from .base import DomainException

class NotificationNotFound(DomainException):
    def __init__(self, notification_id: UUID) -> None:
        super().__init__(f"Notification with id {str(notification_id)} not found.")
