from collections.abc import Generator
from time import monotonic, sleep

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

#This module is responsible for setting up the DB connection
engine: Engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    connect_args={"connect_timeout": settings.database_connect_timeout_seconds},
)

#This creates the sessionmaker for the SQLAlchemy ORM
#This creates the Sessions to interact with the DB
SessionLocal: sessionmaker[Session] = sessionmaker[Session](
    autocommit=False,
    autoflush=False,
    bind=engine,
)

#Method to get a DB session so it can be used by repositories and services
def get_db() -> Generator[Session, None, None]:
    db: Session = SessionLocal()

    try:
        #Yield the DB session to be used in the context of a request
        yield db
    finally:
        #Close the DB session after th request is completed
        db.close()

#This method waits for the database to be available before proceeding
def wait_for_database() -> None:
    deadline = monotonic() + settings.database_connection_timeout_seconds
    last_error: SQLAlchemyError | None = None
    attempt = 1

    while monotonic() < deadline:
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return
        except SQLAlchemyError as error:
            last_error = error
            print(
                "Database connection attempt "
                f"{attempt} failed. Retrying in "
                f"{settings.database_connection_retry_interval_seconds} seconds. "
                f"Error: {error}",
                flush=True,
            )
            attempt += 1
            sleep(settings.database_connection_retry_interval_seconds)

    raise RuntimeError(
        "Database connection could not be established within "
        f"{settings.database_connection_timeout_seconds} seconds."
    ) from last_error
