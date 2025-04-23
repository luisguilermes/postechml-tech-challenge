from flask_restx import Api

from .production_routes import ns as production_ns
from .comercialization_routes import ns as comercialization_ns

def register_routes(app):
    api = Api(
        app,
        version="1.0",
        title="Dados da Vitivinicultura",
        description="API com Dados da Vitivinicultura",
    )
    api.add_namespace(production_ns, path="/api/v1/production")
    api.add_namespace(comercialization_ns, path="/api/v1/comercialization")
