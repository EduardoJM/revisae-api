from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from application.schemas.user import RegisterUserInput
from application.use_cases.user import RegisterUser, AuthenticatedUser
from domain.entities.user import User
from domain.repositories.user_port import UserPort
from domain.value_objects.email import Email
from domain.value_objects.password import HashedPassword
from domain.exceptions.user import EmailAlreadyTaken, UserNotFound
from application.interfaces.hasher_service_port import HasherServicePort
from application.interfaces.event_publisher_port import EventPublisherPort

@pytest.fixture
def user_port(mocker):
    return mocker.create_autospec(UserPort, instance=True)

@pytest.fixture
def event_port(mocker):
    return mocker.create_autospec(EventPublisherPort, instance=True)

@pytest.fixture
def hasher_port(mocker):
    port = mocker.create_autospec(HasherServicePort, instance=True)
    port.hash_password.return_value = "hashed_pw"
    port.verify_password.return_value = True
    return port

@pytest.mark.asyncio
async def test_register_user_saves_and_publishes(user_port, hasher_port, event_port):
    user_port.find_by_email = AsyncMock(return_value=None)
    user_port.save = AsyncMock()
    event_port.publish = AsyncMock()

    use_case = RegisterUser(user_port, hasher_port, event_port)
    result = await use_case.execute(
        RegisterUserInput(email="alice@example.com", password="pass1234", full_name="Alice")
    )

    assert result.email == "alice@example.com"
    user_port.save.assert_called_once()
    event_port.publish.assert_called_once()

@pytest.mark.asyncio
async def test_register_user_raises_if_email_taken(user_port, hasher_port, event_port):
    existing = User.register(uuid4(), Email("alice@example.com"), HashedPassword("x"), "Alice")
    user_port.find_by_email = AsyncMock(return_value=existing)

    use_case = RegisterUser(user_port, hasher_port, event_port)
    with pytest.raises(EmailAlreadyTaken):
        await use_case.execute(
            RegisterUserInput(email="alice@example.com", password="pass1234", full_name="Alice")
        )

@pytest.mark.asyncio
async def test_authenticated_user(user_port):
    existing = User.register(uuid4(), Email("alice@example.com"), HashedPassword("x"), "Alice")
    user_port.find_by_id = AsyncMock(return_value=existing)

    use_case = AuthenticatedUser(user_port)
    result = await use_case.execute(uuid4())

    assert result.email == "alice@example.com"

@pytest.mark.asyncio
async def test_authenticated_user_not_found(user_port):
    user_port.find_by_id = AsyncMock(return_value=None)

    use_case = AuthenticatedUser(user_port)

    with pytest.raises(UserNotFound):
        await use_case.execute(uuid4())
