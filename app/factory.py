from collections.abc import Callable
from contextlib import AbstractAsyncContextManager

from fastapi import FastAPI

from app.core.config import settings


AppLifespan = Callable[[FastAPI], AbstractAsyncContextManager[None]]


def create_app(lifespan: AppLifespan | None = None) -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Backend for managing OCPP charge points.",
        lifespan=lifespan,
    )

    return app
