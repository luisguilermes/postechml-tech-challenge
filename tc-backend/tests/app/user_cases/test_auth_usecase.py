from unittest.mock import MagicMock
from jose import jwt

from app.core.config import settings
from app.use_cases.auth_usecase import AuthUseCase
from app.util.auth_util import pwd_context


def test_authenticate_user_returns_auth_token_for_valid_credentials():
    repo = MagicMock()
    repo.get_by_username.return_value = {
        "username": "user",
        "hashed_password": "hashed_pwd",
    }
    use_case = AuthUseCase(repo)
    pwd_context.verify = MagicMock(return_value=True)

    result = use_case.authenticate_user("user", "password")

    assert result.access_token is not None
    assert result.refresh_token is not None


def test_authenticate_user_raises_not_found_for_invalid_credentials():
    repo = MagicMock()
    repo.get_by_username.return_value = None
    use_case = AuthUseCase(repo)

    try:
        use_case.authenticate_user("invalid_user", "password")
    except Exception as e:
        assert str(e) == "Usuário ou senha inválidos"


def test_refresh_token_returns_new_tokens_for_valid_refresh_token():
    repo = MagicMock()
    repo.get_by_username.return_value = {"username": "user"}
    use_case = AuthUseCase(repo)
    valid_token = jwt.encode(
        {"sub": "user", "type": "refresh"},
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    result = use_case.refresh_token(valid_token)

    assert result.access_token is not None
    assert result.refresh_token is not None


def test_refresh_token_raises_not_found_for_invalid_token_type():
    repo = MagicMock()
    use_case = AuthUseCase(repo)
    invalid_token = jwt.encode(
        {"sub": "user", "type": "access"},
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    try:
        use_case.refresh_token(invalid_token)
    except Exception as e:
        assert str(e) == "Invalid token type"


def test_refresh_token_raises_not_found_for_nonexistent_user():
    repo = MagicMock()
    repo.get_by_username.return_value = None
    use_case = AuthUseCase(repo)
    valid_token = jwt.encode(
        {"sub": "nonexistent_user", "type": "refresh"},
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    try:
        use_case.refresh_token(valid_token)
    except Exception as e:
        assert str(e) == "Usuário ou senha inválidos"
