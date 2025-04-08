from app.adapters.repositories.user_repository_impl import \
    SQLAlchemyUserRepository
from app.infra.db.models import UserModel, db
# from app.infra.security.jwt_service import generate_token
# from app.use_cases.auth_use_case import AuthUseCase
from config.oauth import oauth
from flask import Blueprint, jsonify, redirect, request, url_for

google_bp = Blueprint("google_auth", __name__)
repo = SQLAlchemyUserRepository()
# auth_use_case = AuthUseCase(repo)

@google_bp.route("/auth/google/login")
def google_login():
    redirect_uri = url_for('google_auth.google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@google_bp.route("/auth/google/callback")
def google_callback():
    # token = oauth.google.authorize_access_token()
    # user_info = oauth.google.get('userinfo').json()

    # Tenta encontrar o usuário no banco
    # user = repo.find_by_username(user_info['email'])

    # if not user:
        # Registra automaticamente se não existir
        # user = repo.save(user_info['email'], password_hash='')

    # jwt_token = generate_token(user.id)
    # return jsonify({"token": jwt_token, "email": user.username})
    return jsonify({"message": "Google authentication callback"})