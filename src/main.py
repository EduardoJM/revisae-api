from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from presentation.exception_handlers import register_exception_handlers
from presentation.routers import auth, users, subjects
from infrastructure.providers.providers import (
    DatabaseProvider,
    InfrastructureProvider,
    RepositoryProvider,
    UseCaseProvider,
)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Revisaê - API",
        description="",
        version="1.0.0",
    )

    # ── IoC container ─────────────────────────────────────────────────────────
    container = make_async_container(
        InfrastructureProvider(),
        DatabaseProvider(),
        RepositoryProvider(),
        UseCaseProvider(),
    )
    setup_dishka(container, app)

    # ── Exception handlers ────────────────────────────────────────────────────
    register_exception_handlers(app)

    # ── Routers ───────────────────────────────────────────────────────────────
    prefix = "/api/v1"
    app.include_router(users.router, prefix=prefix)
    app.include_router(auth.router, prefix=prefix)
    app.include_router(subjects.router, prefix=prefix)

    return app


app = create_app()
