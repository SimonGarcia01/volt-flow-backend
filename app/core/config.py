from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

#Uses the BaseSettings to create a Settings so the rest of the app can get the .env variables
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    #All the variables that are taken into the app
    #Can be used as settings.attributeX
    app_name: str = "Volt Flow Backend"
    app_env: str = "development"
    app_version: str = "0.1.0"

    api_host: str = "127.0.0.1"
    api_port: int = 8000
    api_reload: bool = True

    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    database_url_override: str | None = Field(
        default=None,
        validation_alias="DATABASE_URL",
    )
    database_echo: bool = False
    database_pool_size: int = 5
    database_max_overflow: int = 10
    database_connect_timeout_seconds: int = 5
    database_connection_timeout_seconds: int = 15
    database_connection_retry_interval_seconds: int = 2
    create_db_tables_on_startup: bool = True

    #The @property decorator allows us to use the database_url as a property of the settings object
    #This means that we can access the database_url as settings.database_url instead of settings.database_url()
    @property
    def database_url(self) -> str:
        if self.database_url_override:
            return self.database_url_override

        return (
            "postgresql+psycopg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

#The lru chache makes sure that the settings are only loaded once and cached for future use
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings() # type: ignore[call-arg]

settings = get_settings()
