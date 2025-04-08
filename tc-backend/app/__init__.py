from app.web.routes.google_auth_routes import google_bp
from config import Config
from config.oauth import configure_oauth
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    configure_oauth(app)
    app.register_blueprint(google_bp)