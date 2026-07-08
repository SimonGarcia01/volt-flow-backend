from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.core.config import settings
from app.database.base import Base
from app.database.database import engine
from app.factory import create_app


def create_database_tables() -> None:
    import app.auth.models  # noqa: F401

    Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    if settings.create_db_tables_on_startup:
        create_database_tables()

    yield


app = create_app(lifespan=lifespan)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
    )
