from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
)
import pika
from pika.adapters.blocking_connection import BlockingChannel

from infrastructure.config.settings import settings, get_database_url

from application.interfaces.hasher_service_port import HasherServicePort
from application.interfaces.jwt_service_port import JWTServicePort
from application.interfaces.event_publisher_port import EventPublisherPort
from application.interfaces.paginator_port import PaginatorPort

from domain.repositories.user_port import UserPort
from domain.repositories.refresh_token_port import RefreshTokenPort
from domain.repositories.subject_port import SubjectPort
from domain.repositories.revision_cycle_port import RevisionCyclePort

from adapters.services.event_publisher_service import LogEventPublisher
from adapters.services.hasher_service import HasherService
from adapters.services.jwt_service import JWTService
from adapters.services.paginator_service import PaginatorService
from adapters.repositories.user_repository import UserRepository
from adapters.repositories.refresh_token_repository import RefreshTokenRepository
from adapters.repositories.subject_repository import SubjectRepository
from adapters.repositories.revision_cycle_repository import RevisionCycleRepository

from application.use_cases.user import RegisterUser, AuthenticatedUser
from application.use_cases.auth import Login, RefreshTokens, Logout
from application.use_cases.subject import (
    CreateSubject, ListSubjects, GetSubject, UpdateSubject, DeleteSubject
)
from application.use_cases.revision_cycle import (
    CreateRevisionCycle, ListRevisionCycles, GetRevisionCycle,
    UpdateRevisionCycle, DeleteRevisionCycle
)

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

class RabbitMQProvider(Provider):
    @provide(scope=Scope.APP)
    def rabbitmq_connection(self) -> pika.BlockingConnection:
        parameters = pika.URLParameters(settings.broker_url)
        connection = pika.BlockingConnection(parameters)
        # TODO: close connection?
        return connection
    
    @provide(scope=Scope.APP)
    def rabbitmq_channel(self, connection: pika.BlockingConnection) -> BlockingChannel:
        return connection.channel()

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
    def publisher(self, channel: BlockingChannel) -> EventPublisherPort:
        return LogEventPublisher(channel)

    @provide(scope=Scope.REQUEST)
    def paginator(
        self,
        session: AsyncSession,
    ) -> PaginatorPort:
        return PaginatorService(session)

class RepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def user_port(self, session: AsyncSession) -> UserPort:
        return UserRepository(session)

    @provide(scope=Scope.REQUEST)
    def refresh_token_port(self, session: AsyncSession) -> RefreshTokenPort:
        return RefreshTokenRepository(session)
    
    @provide(scope=Scope.REQUEST)
    def subject_port(self, session: AsyncSession, paginator: PaginatorPort) -> SubjectPort:
        return SubjectRepository(session, paginator)
    
    @provide(scope=Scope.REQUEST)
    def revision_cycle_port(self, session: AsyncSession, paginator: PaginatorPort) -> RevisionCyclePort:
        return RevisionCycleRepository(session, paginator)

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

    @provide(scope=Scope.REQUEST)
    def create_subject(self, subject_repo: SubjectPort) -> CreateSubject:
        return CreateSubject(subject_repo)

    @provide(scope=Scope.REQUEST)
    def list_subjects(self, subject_repo: SubjectPort) -> ListSubjects:
        return ListSubjects(subject_repo)

    @provide(scope=Scope.REQUEST)
    def get_subject(self, subject_repo: SubjectPort) -> GetSubject:
        return GetSubject(subject_repo)

    @provide(scope=Scope.REQUEST)
    def delete_subject(self, subject_repo: SubjectPort) -> DeleteSubject:
        return DeleteSubject(subject_repo)

    @provide(scope=Scope.REQUEST)
    def update_subject(self, subject_repo: SubjectPort) -> UpdateSubject:
        return UpdateSubject(subject_repo)

    @provide(scope=Scope.REQUEST)
    def create_revision_cycle(self, revision_cycle_repo: RevisionCyclePort) -> CreateRevisionCycle:
        return CreateRevisionCycle(revision_cycle_repo)

    @provide(scope=Scope.REQUEST)
    def list_revision_cycles(self, revision_cycle_repo: RevisionCyclePort) -> ListRevisionCycles:
        return ListRevisionCycles(revision_cycle_repo)

    @provide(scope=Scope.REQUEST)
    def get_revision_cycle(self, revision_cycle_repo: RevisionCyclePort) -> GetRevisionCycle:
        return GetRevisionCycle(revision_cycle_repo)

    @provide(scope=Scope.REQUEST)
    def delete_revision_cycle(self, revision_cycle_repo: RevisionCyclePort) -> DeleteRevisionCycle:
        return DeleteRevisionCycle(revision_cycle_repo)

    @provide(scope=Scope.REQUEST)
    def update_revision_cycle(self, revision_cycle_repo: RevisionCyclePort) -> UpdateRevisionCycle:
        return UpdateRevisionCycle(revision_cycle_repo)
