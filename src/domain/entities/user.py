from uuid import UUID
from datetime import datetime, UTC
from domain.value_objects.email import Email
from domain.value_objects.password import HashedPassword
from domain.events.base import DomainEvent
from domain.events.user import UserRegistered

class User:
    def __init__(
        self,
        user_id: UUID,
        email: Email,
        hashed_password: HashedPassword,
        full_name: str,
        created_at: datetime | None = None,
    ) -> None:
        self._id = user_id
        self._email = email
        self._hashed_password = hashed_password
        self._full_name = full_name
        self._created_at = created_at or datetime.now(UTC)
        self._events: list[DomainEvent] = []

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def email(self) -> Email:
        return self._email

    @property
    def hashed_password(self) -> HashedPassword:
        return self._hashed_password

    @property
    def full_name(self) -> str:
        return self._full_name

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @classmethod
    def register(
        cls,
        user_id: UUID,
        email: Email,
        hashed_password: HashedPassword,
        full_name: str,
    ) -> "User":
        user = cls(user_id, email, hashed_password, full_name)
        user._events.append(UserRegistered(user_id=user_id, full_name=full_name, email=str(email)))
        return user

    def collect_events(self) -> list[DomainEvent]:
        events, self._events = self._events, []
        return events
