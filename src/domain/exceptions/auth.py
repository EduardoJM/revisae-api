from .base import DomainException

class InvalidToken(DomainException):
    def __init__(self) -> None:
        super().__init__("Token is invalid or expired.")

class RefreshTokenNotFound(DomainException):
    def __init__(self) -> None:
        super().__init__("Refresh token not found or already revoked.")

class InvalidCredentials(DomainException):
    def __init__(self) -> None:
        super().__init__("Invalid email or password.")
