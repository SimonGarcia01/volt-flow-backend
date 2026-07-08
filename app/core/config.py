from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

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
    create_db_tables_on_startup: bool = True

    @property
    def database_url(self) -> str:
        if self.database_url_override:
            return self.database_url_override

        return (
            "postgresql+psycopg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings() # type: ignore[call-arg]

settings = get_settings()
