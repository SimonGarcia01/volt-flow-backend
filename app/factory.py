from collections.abc import Callable
from contextlib import AbstractAsyncContextManager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.ocpp.router import router as ocpp_router


AppLifespan = Callable[[FastAPI], AbstractAsyncContextManager[None]]


def create_app(lifespan: AppLifespan | None = None) -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Backend for managing OCPP charge points.",
        lifespan=lifespan,
    )

    app.include_router(api_router)
    app.include_router(ocpp_router)

    return app
