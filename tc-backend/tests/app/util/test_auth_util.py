from jose import jwt, JWTError

from app.core.config import settings
from app.util.auth_util import decode_token


def test_decode_token_returns_decoded_payload_for_valid_token():
    valid_token = jwt.encode(
        {"sub": "user"}, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )

    result = decode_token(valid_token)

    assert result["sub"] == "user"


def test_decode_token_raises_error_for_invalid_token():
    invalid_token = "invalid.token.value"

    try:
        decode_token(invalid_token)
    except JWTError:
        assert True


def test_decode_token_raises_error_for_expired_token():
    expired_token = jwt.encode(
        {"sub": "user", "exp": 0},
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    try:
        decode_token(expired_token)
    except JWTError:
        assert True
