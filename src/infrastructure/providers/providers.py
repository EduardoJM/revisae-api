from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker

from application.interfaces.hasher_service_port import HasherServicePort
from application.interfaces.jwt_service_port import JWTServicePort
from application.interfaces.event_publisher_port import EventPublisherPort
from domain.repositories.user_port import UserPort
from domain.repositories.refresh_token_port import RefreshTokenPort
from infrastructure.config.settings import settings, get_database_url
from adapters.services.event_publisher_service import LogEventPublisher
from adapters.services.hasher_service import HasherService
from adapters.services.jwt_service import JWTService
from adapters.repositories.user_repository import UserRepository
from adapters.repositories.refresh_token_repository import RefreshTokenRepository

from application.use_cases.user import RegisterUser, AuthenticatedUser
from application.use_cases.auth import Login, RefreshTokens, Logout

class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def engine(self) -> AsyncEngine:
        return create_async_engine(
            get_database_url(),
            pool_pre_ping=True,
            echo=settings.DEBUG,
        )

    @provide(scope=Scope.APP)
    def session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def session(
        self, factory: async_sessionmaker[AsyncSession]
    ) -> AsyncIterator[AsyncSession]:
        async with factory() as session:
            async with session.begin():
                yield session   # commit on success, rollback on exception


class InfrastructureProvider(Provider):
    @provide(scope=Scope.APP)
    def jwt(self) -> JWTServicePort:
        return JWTService(
            secret=settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
            access_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            refresh_expire_days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
        )
    
    @provide(scope=Scope.APP)
    def hasher(self) -> HasherServicePort:
        return HasherService()

    @provide(scope=Scope.APP)
    def publisher(self) -> EventPublisherPort:
        return LogEventPublisher()


class RepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def user_port(self, session: AsyncSession) -> UserPort:
        return UserRepository(session)

    @provide(scope=Scope.REQUEST)
    def refresh_token_port(self, session: AsyncSession) -> RefreshTokenPort:
        return RefreshTokenRepository(session)

class UseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def register_user(
        self,
        user_repo: UserPort,
        hasher: HasherServicePort,
        publisher: EventPublisherPort,
    ) -> RegisterUser:
        return RegisterUser(user_repo, hasher, publisher)

    @provide(scope=Scope.REQUEST)
    def authenticated_user(self, user_repo: UserPort) -> AuthenticatedUser:
        return AuthenticatedUser(user_repo)

    @provide(scope=Scope.REQUEST)
    def login(
        self,
        user_repo: UserPort,
        token_repo: RefreshTokenPort,
        hasher: HasherServicePort,
        jwt: JWTServicePort,
    ) -> Login:
        return Login(user_repo, token_repo, hasher, jwt)

    @provide(scope=Scope.REQUEST)
    def refresh_tokens(
        self,
        token_repo: RefreshTokenPort,
        jwt: JWTServicePort
    ) -> RefreshTokens:
        return RefreshTokens(token_repo, jwt)

    @provide(scope=Scope.REQUEST)
    def logout(self, token_repo: RefreshTokenPort) -> Logout:
        return Logout(token_repo)
