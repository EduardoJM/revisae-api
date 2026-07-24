from types import SimpleNamespace
from uuid import UUID, uuid4
from unittest.mock import AsyncMock

import pytest
from dishka import Provider, Scope, make_async_container, provide
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from application.use_cases.user import RegisterUser, AuthenticatedUser
from application.use_cases.auth import Login, Logout, RefreshTokens
from application.use_cases.notification import (
    GetNotification, ListNotifications, MarkNotificationAsReaded
)
from application.use_cases.revision_cycle import (
    CreateRevisionCycle,
    UpdateRevisionCycle,
    DeleteRevisionCycle,
    ListRevisionCycles,
    GetRevisionCycle
)
from application.use_cases.subject import (
    CreateSubject, UpdateSubject, DeleteSubject, ListSubjects, GetSubject
)
from presentation.exception_handlers import register_exception_handlers
from presentation.routers import (
    auth, users, subjects, revision_cycles, notifications
)
from presentation.dependencies import get_current_user_id

AUTHED_USER_ID: UUID = uuid4()

@pytest.fixture
def uc():
    def _uc(cls):
        mock = AsyncMock(spec=cls)
        mock.execute = AsyncMock()
        return mock

    return SimpleNamespace(
        register_user=_uc(RegisterUser),
        authenticated_user=_uc(AuthenticatedUser),
        login=_uc(Login),
        refresh_tokens=_uc(RefreshTokens),
        logout=_uc(Logout),
        create_subject=_uc(CreateSubject),
        update_subject=_uc(UpdateSubject),
        delete_subject=_uc(DeleteSubject),
        list_subjects=_uc(ListSubjects),
        get_subject=_uc(GetSubject),
        create_revision_cycle=_uc(CreateRevisionCycle),
        update_revision_cycle=_uc(UpdateRevisionCycle),
        delete_revision_cycle=_uc(DeleteRevisionCycle),
        get_revision_cycle=_uc(GetRevisionCycle),
        list_revision_cycles=_uc(ListRevisionCycles),
        get_notification=_uc(GetNotification),
        list_notifications=_uc(ListNotifications),
        mark_notification_as_readed=_uc(MarkNotificationAsReaded),
    )

def _make_provider(m: SimpleNamespace) -> Provider:
    """Build a Dishka Provider that serves mock use-case instances."""

    class _TestProvider(Provider):
        scope = Scope.APP

        @provide
        def _register_user(self) -> RegisterUser:
            return m.register_user

        @provide
        def _authenticated_user(self) -> Login:
            return m.authenticated_user
        
        @provide
        def _login(self) -> Login:
            return m.login

        @provide
        def _refresh_tokens(self) -> RefreshTokens:
            return m.refresh_tokens

        @provide
        def _logout(self) -> Logout:
            return m.logout
        
        @provide
        def _create_subject(self) -> CreateSubject:
            return m.create_subject

        @provide
        def _update_subject(self) -> UpdateSubject:
            return m.update_subject

        @provide
        def _delete_subject(self) -> DeleteSubject:
            return m.delete_subject

        @provide
        def _list_subjects(self) -> ListSubjects:
            return m.list_subjects

        @provide
        def _get_subject(self) -> GetSubject:
            return m.get_subject

        @provide
        def _create_revision_cycle(self) -> CreateRevisionCycle:
            return m.create_revision_cycle

        @provide
        def _update_revision_cycle(self) -> UpdateRevisionCycle:
            return m.update_revision_cycle

        @provide
        def _delete_revision_cycle(self) -> DeleteRevisionCycle:
            return m.delete_revision_cycle

        @provide
        def _get_revision_cycle(self) -> GetRevisionCycle:
            return m.get_revision_cycle

        @provide
        def _list_revision_cycles(self) -> ListRevisionCycles:
            return m.list_revision_cycles

        @provide
        def _get_notification(self) -> GetNotification:
            return m.get_notification

        @provide
        def _list_notifications(self) -> ListNotifications:
            return m.list_notifications

        @provide
        def _mark_notification_as_readed(self) -> MarkNotificationAsReaded:
            return m.mark_notification_as_readed


    return _TestProvider()

@pytest.fixture
async def client(uc):
    """Async HTTP client wired to a test FastAPI app with mocked use cases."""
    container = make_async_container(_make_provider(uc))

    app = FastAPI()
    setup_dishka(container, app)
    register_exception_handlers(app)

    prefix = "/api/v1"
    app.include_router(users.router, prefix=prefix)
    app.include_router(auth.router, prefix=prefix)
    app.include_router(subjects.router, prefix=prefix)
    app.include_router(revision_cycles.router, prefix=prefix)
    app.include_router(notifications.router, prefix=prefix)

    # Bypass JWT auth — all requests are authenticated as AUTHED_USER_ID
    app.dependency_overrides[get_current_user_id] = lambda: AUTHED_USER_ID

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    