from uuid import UUID
from datetime import datetime, UTC
from domain.value_objects.hex_color import HexColor

class Subject:
    def __init__(
        self,
        subject_id: UUID,
        user_id: UUID,
        name: str,
        color: HexColor,
        created_at: datetime | None = None,
    ) -> None:
        self._id = subject_id
        self._user_id = user_id
        self._name = name
        self._color = color
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
    def color(self) -> HexColor:
        return self._color

    @property
    def created_at(self) -> datetime:
        return self._created_at

    def update(
        self,
        name: str | None = None,
        color: HexColor | None = None,
    ) -> None:
        if name is not None:
            self._name = name
        if color is not None:
            self._color = color

    def belongs_to(self, user_id: UUID) -> bool:
        return self._user_id == user_id
