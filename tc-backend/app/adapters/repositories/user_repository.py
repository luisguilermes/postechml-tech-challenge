from app.interfaces.repository import UserRepository
from app.util.auth_util import pwd_context

fake_user_db = {
    "user": {"username": "user", "hashed_password": pwd_context.hash("pass")}
}


class UserRepositoryImpl(UserRepository):
    def get_by_username(self, username: str):
        """Get user by username"""
        user = fake_user_db.get(username)
        if user:
            return {
                "username": user["username"],
                "hashed_password": user["hashed_password"],
            }
        return None
