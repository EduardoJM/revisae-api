from uuid import UUID
from datetime import datetime, UTC

class Notification:
    def __init__(
        self,
        notification_id: UUID,
        user_id: UUID,
        title: str,
        description: str,
        is_readed: bool,
        created_at: datetime | None = None,
    ) -> None:
        self._id = notification_id
        self._user_id = user_id
        self._title = title
        self._description = description
        self._is_readed = is_readed
        self._created_at = created_at or datetime.now(UTC)

    @property
    def id(self) -> UUID:
        return self._id
    
    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description
    
    @property
    def is_readed(self) -> bool:
        return self._is_readed

    @property
    def created_at(self) -> datetime:
        return self._created_at

    def belongs_to(self, user_id: UUID) -> bool:
        return self._user_id == user_id

    def mark_as_readed(self):
        self._is_readed = True
