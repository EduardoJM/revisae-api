from uuid import UUID
from dataclasses import dataclass

from .base import DomainEvent

@dataclass(frozen=True)
class SubjectCreated(DomainEvent):
    subject_id: UUID
    user_id: UUID
    subject_name: str
