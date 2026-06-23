from uuid import UUID, uuid4

from domain.repositories.user_port import UserPort
from domain.exceptions.user import EmailAlreadyTaken, UserNotFound
from domain.entities.user import User
from domain.value_objects.email import Email
from domain.value_objects.password import HashedPassword
from application.interfaces.event_publisher_port import EventPublisherPort
from application.interfaces.hasher_service_port import HasherServicePort
from application.schemas.user import UserOutput, RegisterUserInput

def _user_to_output(user: User) -> UserOutput:
    return UserOutput(
        id=user.id,
        email=str(user.email),
        full_name=user.full_name,
        created_at=user.created_at,
    )

class RegisterUser:
    def __init__(
        self,
        user_repo: UserPort,
        hasher: HasherServicePort,
        publisher: EventPublisherPort,
    ) -> None:
        self._users = user_repo
        self._hasher = hasher
        self._publisher = publisher

    async def execute(self, data: RegisterUserInput) -> UserOutput:
        existing = await self._users.find_by_email(data.email.lower())
        if existing:
            raise EmailAlreadyTaken(data.email)

        hashed = self._hasher.hash_password(data.password)
        user = User.register(
            user_id=uuid4(),
            email=Email(data.email),
            hashed_password=HashedPassword(hashed),
            full_name=data.full_name,
        )
        await self._users.save(user)

        for event in user.collect_events():
            await self._publisher.publish(event)

        return _user_to_output(user)

class AuthenticatedUser:
    def __init__(self, user_repo: UserPort):
        self._users = user_repo

    async def execute(self, user_id: UUID) -> UserOutput:
        user = await self._users.find_by_id(user_id)
        if not user:
            raise UserNotFound()
        return _user_to_output(user)
