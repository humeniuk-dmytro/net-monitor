from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@db:5432/netmonitor"
    sync_database_url: str = "postgresql+psycopg2://postgres:postgres@db:5432/netmonitor"
    ping_interval_seconds: int = 30

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()