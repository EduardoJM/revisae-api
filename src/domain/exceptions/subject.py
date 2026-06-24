from uuid import UUID

from .base import DomainException

class SubjectNotFound(DomainException):
    def __init__(self, subject_id: UUID) -> None:
        super().__init__(f"Subject with id {str(subject_id)} not found.")
