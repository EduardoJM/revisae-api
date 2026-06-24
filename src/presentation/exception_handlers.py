from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from domain.exceptions.base import DomainException
from domain.exceptions.auth import (
    InvalidCredentials, InvalidToken, RefreshTokenNotFound
)
from domain.exceptions.user import EmailAlreadyTaken, UserNotFound
from domain.exceptions.subject import SubjectNotFound

def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(EmailAlreadyTaken)
    async def email_taken(_: Request, exc: EmailAlreadyTaken) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(InvalidCredentials)
    async def invalid_credentials(_: Request, exc: InvalidCredentials) -> JSONResponse:
        return JSONResponse(status_code=401, content={"detail": str(exc)})

    @app.exception_handler(UserNotFound)
    async def user_not_found(_: Request, exc: UserNotFound) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(SubjectNotFound)
    async def subject_not_found(_: Request, exc: SubjectNotFound) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(InvalidToken)
    async def invalid_token(_: Request, exc: InvalidToken) -> JSONResponse:
        return JSONResponse(
            status_code=401,
            content={"detail": str(exc)},
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(RefreshTokenNotFound)
    async def refresh_token_not_found(_: Request, exc: RefreshTokenNotFound) -> JSONResponse:
        return JSONResponse(status_code=401, content={"detail": str(exc)})

    @app.exception_handler(DomainException)
    async def generic_domain(_: Request, exc: DomainException) -> JSONResponse:
        """Catch-all for any unhandled domain exception."""
        return JSONResponse(status_code=400, content={"detail": str(exc)})
