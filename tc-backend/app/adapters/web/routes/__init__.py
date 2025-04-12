from flask_restx import Api

from .product_routes import ns as product_ns


def register_routes(app):
    api = Api(app, version="1.0", title="Grape API", description="A Grape API")
    api.add_namespace(product_ns, path="/api/v1/product")