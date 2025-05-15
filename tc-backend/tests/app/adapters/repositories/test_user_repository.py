from app.adapters.repositories.user_repository import UserRepositoryImpl


def test_get_by_username_returns_user_when_username_exists():
    repo = UserRepositoryImpl()
    result = repo.get_by_username("user")
    assert result is not None
    assert result["username"] == "user"
    assert "hashed_password" in result


def test_get_by_username_returns_none_when_username_does_not_exist():
    repo = UserRepositoryImpl()
    result = repo.get_by_username("nonexistent_user")
    assert result is None
