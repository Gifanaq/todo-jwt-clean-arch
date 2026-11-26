from functools import lru_cache
from typing import Annotated

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = Field(min_length=1)
    access_secret: SecretStr = Field(min_length=32)
    refresh_secret: SecretStr = Field(min_length=32)
    access_ttl_minutes: Annotated[int, Field(gt=0)] = 15
    refresh_ttl_days: Annotated[int, Field(gt=0)] = 30
    cookie_secure: bool = False
    cors_origins: list[str] = ["http://localhost:5173"]


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
