from uuid import UUID

from .base import DomainException

class RevisionCycleNotFound(DomainException):
    def __init__(self, subject_id: UUID) -> None:
        super().__init__(f"Revision cycle with id {str(subject_id)} not found.")
