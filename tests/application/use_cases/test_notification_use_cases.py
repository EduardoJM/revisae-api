from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from application.use_cases.notification import (
    GetNotification, ListNotifications, MarkNotificationAsReaded
)
from domain.entities.notification import Notification
from domain.exceptions.notification import NotificationNotFound
from domain.repositories.notification_port import NotificationPort
from application.interfaces.paginator_port import Page

@pytest.fixture
def notification_port(mocker):
    return mocker.create_autospec(NotificationPort, instance=True)

@pytest.mark.asyncio
async def test_get_notification_without_found(notification_port):
    notification_port.find_by_id = AsyncMock(return_value=None)

    use_case = GetNotification(notification_port)

    with pytest.raises(NotificationNotFound):
        await use_case.execute(uuid4(), uuid4())

@pytest.mark.asyncio
async def test_get_notification_with_not_belongs_to_user(notification_port):
    user_id = uuid4()
    notification = Notification(uuid4(), user_id, 'Notification', 'Description', False)
    notification_port.find_by_id = AsyncMock(return_value=notification)

    use_case = GetNotification(notification_port)

    with pytest.raises(NotificationNotFound):
        await use_case.execute(uuid4(), uuid4())

@pytest.mark.asyncio
async def test_get_notification_with_found(notification_port):
    user_id = uuid4()
    notification = Notification(uuid4(), user_id, 'Notification', 'Description', False)
    notification_port.find_by_id = AsyncMock(return_value=notification)

    use_case = GetNotification(notification_port)

    result = await use_case.execute(user_id, uuid4())

    assert result.title == 'Notification'
    assert result.description == 'Description'
    assert result.is_readed == False

@pytest.mark.asyncio
async def test_mark_notification_as_readed_not_found(notification_port):
    notification_port.find_by_id = AsyncMock(return_value=None)

    use_case = MarkNotificationAsReaded(notification_port)

    with pytest.raises(NotificationNotFound):
        await use_case.execute(uuid4(), uuid4())

@pytest.mark.asyncio
async def test_mark_notification_as_readed_not_belongs_to_user(notification_port):
    user_id = uuid4()
    notification = Notification(uuid4(), user_id, 'Notification', 'Description', False)
    notification_port.find_by_id = AsyncMock(return_value=notification)

    use_case = MarkNotificationAsReaded(notification_port)

    with pytest.raises(NotificationNotFound):
        await use_case.execute(uuid4(), uuid4())

@pytest.mark.asyncio
async def test_mark_notification_as_readed(notification_port):
    user_id = uuid4()
    notification = Notification(uuid4(), user_id, 'Notification', 'Description', False)
    notification_port.find_by_id = AsyncMock(return_value=notification)

    use_case = MarkNotificationAsReaded(notification_port)

    result = await use_case.execute(user_id, uuid4())

    assert result.title == 'Notification'
    assert result.description == 'Description'
    assert result.is_readed == True

@pytest.mark.asyncio
async def test_list_notifications(notification_port):
    notification = Notification(uuid4(), uuid4(), 'Notification', 'Description', False)
    page = Page(results=[notification], total=10, per_page=5)
    notification_port.find_by_user_paginated = AsyncMock(return_value=page)

    user_id = uuid4()
    notification = Notification(uuid4(), user_id, 'Notification', 'Description', False)
    notification_port.find_by_id = AsyncMock(return_value=notification)

    use_case = ListNotifications(notification_port)

    result = await use_case.execute(uuid4(), 5, 10, '')

    assert result.total == 10
    assert result.per_page == 5
    assert len(result.results) == 1
    assert result.results[0].title == 'Notification'
