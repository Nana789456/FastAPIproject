import os
from dataclasses import dataclass
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str  # соответствует DATABASE_URL в .env

    # Аутентификация (JWT)
    secret_key: str  # соответствует SECRET_KEY в .env
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    # На проде за HTTPS — true; false нужен только для локального HTTP не на localhost
    refresh_cookie_secure: bool = True

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()
