from pydantic import Field, AnyHttpUrl
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )
    auth_key: str = "xxx"
    APP_NAME: str = "AI Agent Backend"
    ENVIRONMENT: Literal["local", "dev", "staging", "prod"] = "local"
    API_V1_PREFIX: str = "/api/v1"

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] | list[str] = Field(
        default_factory=lambda: ["http://localhost:3000"]
    )
    redis_port: str = "6379"
    redis_host: str = "localhost"
    # Logging
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    # Model provider selection
    MODEL_PROVIDER: Literal["gemini", "openai", "mistral"] = "gemini"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
