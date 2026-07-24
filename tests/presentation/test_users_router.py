from uuid import uuid4
from datetime import datetime, UTC

import pytest

from application.schemas.user import UserOutput
from domain.exceptions.user import EmailAlreadyTaken

from .conftest import AUTHED_USER_ID

def _user_output(**kwargs) -> UserOutput:
    defaults = dict(
        id=uuid4(),
        email="alice@example.com",
        full_name="Alice Silva",
        created_at=datetime.now(UTC),
    )
    return UserOutput(**{**defaults, **kwargs})

@pytest.mark.asyncio
async def test_register_user_returns_201(client, uc):
    uc.register_user.execute.return_value = _user_output()

    resp = await client.post(
        "/api/v1/users/",
        json={"email": "alice@example.com", "password": "s3cur3P@ss", "full_name": "Alice Silva"},
    )

    assert resp.status_code == 201
    body = resp.json()
    assert body["email"] == "alice@example.com"
    assert body["full_name"] == "Alice Silva"
    uc.register_user.execute.assert_called_once()

@pytest.mark.asyncio
async def test_register_user_returns_409_when_email_taken(client, uc):
    uc.register_user.execute.side_effect = EmailAlreadyTaken("alice@example.com")

    resp = await client.post(
        "/api/v1/users/",
        json={"email": "alice@example.com", "password": "s3cur3P@ss", "full_name": "Alice Silva"},
    )

    assert resp.status_code == 409
    assert "already registered" in resp.json()["detail"]

@pytest.mark.asyncio
async def test_register_user_returns_422_when_password_too_short(client, uc):
    resp = await client.post(
        "/api/v1/users/",
        json={"email": "alice@example.com", "password": "short", "full_name": "Alice"},
    )

    assert resp.status_code == 422
    uc.register_user.execute.assert_not_called()
    
@pytest.mark.asyncio
async def test_register_user_returns_422_when_email_invalid(client, uc):
    resp = await client.post(
        "/api/v1/users/",
        json={"email": "not-an-email", "password": "s3cur3P@ss", "full_name": "Alice"},
    )

    assert resp.status_code == 422
    uc.register_user.execute.assert_not_called()
    