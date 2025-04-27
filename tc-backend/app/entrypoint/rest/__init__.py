from flask_restx import Api
from app.entrypoint.rest.product_routes import register_product_resource, get_production_service, get_processing_service


def register_routes(app):
    api = Api(
        app,
        version="1.0",
        title="Dados da Vitivinicultura",
        description="API com Dados da Vitivinicultura",
    )
    api.add_namespace(
        register_product_resource(
            "/api/v1/products/production",
            "Produção de vinhos, sucos e derivados do Rio Grande do Sul",
            get_production_service,
        )
    )

    api.add_namespace(
        register_product_resource(
            "/api/v1/products/processing",
            "Processamento de vinhos, sucos e derivados do Rio Grande do Sul",
            get_processing_service,
        )
    )
