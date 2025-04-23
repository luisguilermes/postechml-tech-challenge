from flask_restx import Namespace, Resource, fields, reqparse
from app.adapters.repositories.scrapers.comercialization_embrapa_scraper import (
    ComercializationEmbrapaScraper,
)
from app.domain.services.comercialization_service import ComercializationService
from app.domain.vo.product_filter import Filter


# Namespace definition
ns = Namespace(
    "comercialization",
    description="Comercialização de vinhos, sucos e derivados do Rio Grande do Sul",
)

# Model definition for API response
model = ns.model(
    "Model",
    {
        "id": fields.String,
        "amount": fields.Float,
        "unit": fields.String,
        "category": fields.String,
        "sub_category": fields.String,
        "source": fields.String,
        "collected_at": fields.DateTime,
        "year": fields.Integer,
    },
)

# Request parser for query parameters
parser = reqparse.RequestParser()
parser.add_argument("category", type=str, required=False, help="Filter by category")
parser.add_argument(
    "year", type=int, required=False, help="Filter by year", default=2023
)


# Factory function to create the service
def get_production_service():
    repo = ComercializationEmbrapaScraper()
    return ComercializationService(repo)


# Resource definition
@ns.route("")
class ComercializationResource(Resource):
    @ns.expect(parser)
    @ns.marshal_with(model, as_list=True, code=200)
    def get(self):
        # Parse query parameters
        args = parser.parse_args()
        year = args.get("year", 2023)
        category = args.get("category", None)

        # Create filter and service
        product_filter = Filter(category=category)
        service = get_production_service()

        # Fetch and return products
        return service.get_all_products(year=year, product_filter=product_filter)
