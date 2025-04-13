from app.entrypoint.rest.routes import register_routes
from flask import Flask


def create_app():
    app = Flask(__name__)

    # Register blueprints
    register_routes(app)

    return app
