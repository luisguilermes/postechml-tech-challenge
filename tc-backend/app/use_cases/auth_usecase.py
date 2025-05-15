from datetime import datetime, timedelta

from jose import jwt

from app.core.config import settings
from app.interfaces.repository import UserRepository
from app.models.auth import AuthToken
from app.models.exception import NotFoundException
from app.util.auth_util import pwd_context


def _verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def _create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(
        to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


def _create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(
        to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


class AuthUseCase:
    error_message = "Usuário ou senha inválidos"

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def authenticate_user(self, username: str, password: str) -> AuthToken:
        user = self.repo.get_by_username(username)
        if not user or not _verify_password(password, user["hashed_password"]):
            raise NotFoundException(status_code=401, detail=self.error_message)
        access_token = _create_access_token({"sub": user["username"]})
        refresh_token = _create_refresh_token({"sub": user["username"]})
        return AuthToken(access_token=access_token, refresh_token=refresh_token)

    def refresh_token(self, token: str) -> AuthToken:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        if payload.get("type") != "refresh":
            raise NotFoundException(status_code=403, detail="Invalid token type")
        username = payload.get("sub")
        user = self.repo.get_by_username(username)
        if not user:
            raise NotFoundException(status_code=401, detail=self.error_message)
        access_token = _create_access_token({"sub": user["username"]})
        refresh_token = _create_refresh_token({"sub": user["username"]})
        return AuthToken(access_token=access_token, refresh_token=refresh_token)
