from uuid import UUID

from .base import DomainException

class EmailAlreadyTaken(DomainException):
    def __init__(self, email: str) -> None:
        super().__init__(f"Email '{email}' is already registered.")

class UserNotFound(DomainException):
    def __init__(self, user_id: UUID) -> None:
        super().__init__(f"User with id {str(user_id)} not found.")
