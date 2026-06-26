from uuid import UUID
from dataclasses import dataclass

from .base import DomainEvent

@dataclass(frozen=True)
class UserRegistered(DomainEvent):
    user_id: UUID
    email: str
    full_name: str
