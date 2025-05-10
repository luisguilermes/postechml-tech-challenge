from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FTM Backend App"
    version: str = "1.0.0"
    env: str = "development"
    port: int = 8000

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    allowed_hosts: List[str] = ["*"]

    database_url: str = "sqlite:///./tc-backend.db"

    class Config:
        env_file = ".env"


settings = Settings()
