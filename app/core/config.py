from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    mongo_uri: str
    mongo_database_name: str
    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
