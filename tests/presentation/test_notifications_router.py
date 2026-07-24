from uuid import uuid4
from datetime import datetime, UTC

import pytest

from application.schemas.notification import NotificationOutput, PaginatedNotificationOutput

from .conftest import AUTHED_USER_ID

def _notification_output(**kwargs) -> NotificationOutput:
    defaults = dict(
        id=uuid4(),
        user_id=uuid4(),
        title='Notification',
        description='Description',
        is_readed=False,
        created_at=datetime.now(UTC),
    )
    return NotificationOutput(**{**defaults, **kwargs})

def _notification_list_output(notification_kwargs = None, **kwargs) -> NotificationOutput:
    defaults = dict(
        id=uuid4(),
        user_id=uuid4(),
        title='Notification',
        description='Description',
        is_readed=False,
        created_at=datetime.now(UTC),
    )
    return PaginatedNotificationOutput(
        results=[{**defaults, **(notification_kwargs or {})}],
        **{**kwargs, 'total': 55, 'per_page': 10},
    )

@pytest.mark.asyncio
async def test_list_notifications_returns_200(client, uc):
    uc.list_notifications.execute.return_value = _notification_list_output()

    resp = await client.get("/api/v1/notifications/")

    assert resp.status_code == 201
    body = resp.json()
    assert body['total'] == 55
    assert body['per_page'] == 10
    assert len(body['results']) == 1
    assert body['results'][0]['title'] == 'Notification'
    assert body['results'][0]['description'] == 'Description'
    uc.list_notifications.execute.assert_called_once()
