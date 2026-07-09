from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.core.config import settings
from app.database.base import Base
from app.database.database import engine, wait_for_database
from app.database.model_registry import import_all_models
from app.factory import create_app

#Method that creates the database tables based on the defined models in the app
def create_database_tables() -> None:
    import_all_models()
    Base.metadata.create_all(bind=engine)

#This is an async context manager that defines the lifespan of the FastAPI app
#It checks if the setting to create a DB tables on startup is enabled, if so, it calls create_database_tables()
#After the setup, it yields control back to the FastAPI app, allowing it to run
#When the app shuts down, the context manager will exit
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    wait_for_database()

    if settings.create_db_tables_on_startup:
        create_database_tables()

    yield

#Actual main entry point of the application
app = create_app(lifespan=lifespan)

#Block checks it the file is being run as the main program
#It then runs the uvicorn server with the specified host, port and reload settings from the configuration
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
    )

@app.get("/")
async def root():
    return {"status": "running"}