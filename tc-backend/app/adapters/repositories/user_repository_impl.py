from app.domain.repositories.user_repository import UserRepository
from app.infra.db.models import UserModel, db


class SQLAlchemyUserRepository(UserRepository):
    def find_by_username(self, username: str):
        return UserModel.query.filter_by(username=username).first()

    def save(self, username: str, password_hash: str):
        user = UserModel(username=username, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return user