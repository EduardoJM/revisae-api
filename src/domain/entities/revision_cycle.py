from uuid import UUID
from datetime import datetime, UTC

class RevisionCycle:
    def __init__(
        self,
        revision_cycle_id: UUID,
        user_id: UUID,
        name: str,
        days: list[int],
        created_at: datetime | None = None,
    ) -> None:
        self._id = revision_cycle_id
        self._user_id = user_id
        self._name = name
        self._days = days
        self._created_at = created_at or datetime.now(UTC)

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def days(self) -> list[int]:
        return self._days

    @property
    def created_at(self) -> datetime:
        return self._created_at

    def update(
        self,
        name: str | None = None,
        days: list[int] | None = None,
    ) -> None:
        if name is not None:
            self._name = name
        if days is not None:
            self._days = days

    def belongs_to(self, user_id: UUID) -> bool:
        return self._user_id == user_id
