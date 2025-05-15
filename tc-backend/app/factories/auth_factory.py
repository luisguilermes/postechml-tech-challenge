from app.factories.user_factory import get_user_repository
from app.use_cases.auth_usecase import AuthUseCase


def get_auth_use_case():
    return AuthUseCase(get_user_repository())
