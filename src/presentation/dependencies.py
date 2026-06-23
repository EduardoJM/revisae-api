from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from application.interfaces.jwt_service_port import JWTServicePort
from domain.exceptions.auth import InvalidToken

_bearer = HTTPBearer()


@inject
async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    jwt: FromDishka[JWTServicePort] = None,  # type: ignore[assignment]
) -> UUID:
    try:
        payload = jwt.decode_token(credentials.credentials)
        return UUID(payload["sub"])
    except (InvalidToken, KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
