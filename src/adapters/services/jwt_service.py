import hashlib
import secrets
from datetime import datetime, timedelta, UTC
from uuid import UUID

from jose import jwt, JWTError

from application.interfaces.jwt_service_port import JWTServicePort
from domain.exceptions.auth import InvalidToken


class JWTService(JWTServicePort):
    def __init__(self, secret: str, algorithm: str, access_expire_minutes: int, refresh_expire_days: int) -> None:
        self._secret = secret
        self._algorithm = algorithm
        self._access_expire = timedelta(minutes=access_expire_minutes)
        self._refresh_expire = timedelta(days=refresh_expire_days)

    def create_access_token(self, user_id: UUID) -> str:
        now = datetime.now(UTC)
        payload = {
            "sub": str(user_id),
            "type": "access",
            "iat": now,
            "exp": now + self._access_expire,
        }
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)

    def create_refresh_token(self, user_id: UUID) -> tuple[str, str, datetime]:
        raw = secrets.token_urlsafe(48)
        token_hash = hashlib.sha256(raw.encode()).hexdigest()
        expires_at = datetime.now(UTC) + self._refresh_expire
        return raw, token_hash, expires_at

    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self._secret, algorithms=[self._algorithm])
            if payload.get("type") != "access":
                raise InvalidToken()
            return payload
        except JWTError:
            raise InvalidToken()
