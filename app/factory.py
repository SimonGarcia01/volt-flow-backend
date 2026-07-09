from collections.abc import Callable
from contextlib import AbstractAsyncContextManager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.ocpp.router import router as ocpp_router

#AppLifespan is an alias for a callable that takes a FastAPI instance and returns an abstract async context manager
#This is used to define the lifespan of the FastAPI application, allowing for setup and teardown operations during the application's lifecycle
AppLifespan = Callable[[FastAPI], AbstractAsyncContextManager[None]]

#Creates the FastAPI application instance with the specified lifespan context manager
#It includes the API router and OCPP router for handling requests related to auth, charing and OCPP charge points
def create_app(lifespan: AppLifespan | None = None) -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Backend for managing OCPP charge points.",
        lifespan=lifespan,
    )

    #Include here all the routers for the application
    app.include_router(api_router)
    app.include_router(ocpp_router)

    return app
