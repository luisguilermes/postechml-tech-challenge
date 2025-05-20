from typing import List

from pydantic_settings import BaseSettings

# Defina o arquivo .env dinamicamente antes da definição da classe
env_file_path = ".env"


class Settings(BaseSettings):
    app_name: str = "FTM Backend App"
    version: str = "1.0.0"
    env: str = "development"
    port: int = 8000

    jwt_secret_key: str = "your_jwt_secret_key"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    allowed_hosts: List[str] = ["*"]

    database_url: str = "sqlite:///./tc-backend.db"

    embrapa_url: str = "http://vitibrasil.cnpuv.embrapa.br/index.php"
    embrapa_connection_timeout: int = 10  # segundos pra conectar
    embrapa_read_timeout: int = 20  # segundos pra ler a resposta

    class Config:
        env_file = env_file_path


settings = Settings()
