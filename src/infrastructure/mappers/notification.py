from domain.entities.notification import Notification
from infrastructure.database.models.notification import NotificationModel


class NotificationMapper:
    @staticmethod
    def to_entity(row: NotificationModel) -> Notification:
        return Notification(
            notification_id=row.id,
            user_id=row.user_id,
            title=row.title,
            description=row.description,
            is_readed=row.is_readed,
            created_at=row.created_at,
        )

    @staticmethod
    def to_model(notification: Notification) -> NotificationModel:
        return NotificationModel(
            id=notification.id,
            user_id=notification.user_id,
            title=notification.title,
            description=notification.description,
            is_readed=notification.is_readed,
            created_at=notification.created_at,
        )
