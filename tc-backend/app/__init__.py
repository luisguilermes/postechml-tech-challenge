from flask import Flask

from app.adapters.web.routes import register_routes


def create_app():
    app = Flask(__name__)

    # Register blueprints
    register_routes(app)

    return app
