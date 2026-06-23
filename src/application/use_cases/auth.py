from uuid import UUID

from domain.repositories.user_repository_port import UserRepositoryPort
from domain.repositories.refresh_token_repository_port import RefreshTokenRepositoryPort
from domain.exceptions.auth import RefreshTokenNotFound, InvalidCredentials
from application.interfaces.hasher_service_port import HasherServicePort
from application.interfaces.jwt_service_port import JWTServicePort
from application.schemas.auth import RefreshInput, LoginInput, TokenOutput

class Login:
    def __init__(
        self,
        user_repo: UserRepositoryPort,
        token_repo: RefreshTokenRepositoryPort,
        hasher: HasherServicePort,
        jwt: JWTServicePort,
    ) -> None:
        self._users = user_repo
        self._tokens = token_repo
        self._hasher = hasher
        self._jwt = jwt

    async def execute(self, data: LoginInput) -> TokenOutput:
        user = await self._users.find_by_email(data.email.lower())
        if not user:
            raise InvalidCredentials()
        if not self._hasher.verify_password(data.password, str(user.hashed_password)):
            raise InvalidCredentials()

        access = self._jwt.create_access_token(user.id)
        raw_refresh, token_hash, expires_at = self._jwt.create_refresh_token(user.id)
        await self._tokens.save(user.id, token_hash, expires_at)

        return TokenOutput(access_token=access, refresh_token=raw_refresh)

class RefreshTokens:
    def __init__(
        self,
        token_repo: RefreshTokenRepositoryPort,
        jwt: JWTServicePort,
    ) -> None:
        self._tokens = token_repo
        self._jwt = jwt

    async def execute(self, data: RefreshInput) -> TokenOutput:
        import hashlib
        token_hash = hashlib.sha256(data.refresh_token.encode()).hexdigest()
        record = await self._tokens.find(token_hash)
        if not record:
            raise RefreshTokenNotFound()

        await self._tokens.revoke(token_hash)
        user_id = UUID(record["user_id"])

        access = self._jwt.create_access_token(user_id)
        raw_refresh, new_hash, expires_at = self._jwt.create_refresh_token(user_id)
        await self._tokens.save(user_id, new_hash, expires_at)

        return TokenOutput(access_token=access, refresh_token=raw_refresh)

class Logout:
    def __init__(self, token_repo: RefreshTokenRepositoryPort) -> None:
        self._tokens = token_repo

    async def execute(self, data: RefreshInput) -> None:
        import hashlib
        token_hash = hashlib.sha256(data.refresh_token.encode()).hexdigest()
        record = await self._tokens.find(token_hash)
        if not record:
            raise RefreshTokenNotFound()
        await self._tokens.revoke(token_hash)
