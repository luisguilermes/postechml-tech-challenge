from app.adapters.repositories.user_repository import UserRepositoryImpl
from app.interfaces.repository import UserRepository


def get_user_repository() -> UserRepository:
    return UserRepositoryImpl()
