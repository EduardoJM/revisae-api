from .base import DomainException

class EmailAlreadyTaken(DomainException):
    def __init__(self, email: str) -> None:
        super().__init__(f"Email '{email}' is already registered.")

