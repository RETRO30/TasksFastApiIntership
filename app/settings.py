import redis.asyncio as aioredis 

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import (
    RedisDsn,
    Field
)


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="AUTH__",
    )

    secret_key: str
    expire_minutes: int = 30


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        env_prefix="API__",
    )

    redis_url: RedisDsn
    auth: AuthSettings = Field(default_factory=AuthSettings)


settings = Settings()
redis_client = aioredis.from_url(str(settings.redis_url), decode_responses=True)


if __name__ == "__main__":
    print(settings)
