from flask_restx import Namespace, Resource, fields, reqparse
from app.adapters.repositories.scrapers.importing_embrapa_scraper import (
    ImportingEmbrapaScraper,
)
from app.domain.services.importing_service import ImportingService
from app.domain.vo.product2_filter import Filter


# Namespace definition
ns = Namespace(
    "importing",
    description="Importação de vinhos, sucos e derivados do Rio Grande do Sul",
)

# Model definition for API response
model = ns.model(
    "Model",
    {
        "id": fields.String,
        "country": fields.String,
        "quantity": fields.Integer,
        "dollar": fields.Float,
        "source": fields.String,
        "collected_at": fields.DateTime,
        "year": fields.Integer,
    },
)

# Request parser for query parameters
parser = reqparse.RequestParser()
parser.add_argument("country", type=str, required=False, help="Filter by country")
parser.add_argument(
    "year", type=int, required=False, help="Filter by year", default=2024
)


# Factory function to create the service
def get_importing_service():
    repo = ImportingEmbrapaScraper()
    return ImportingService(repo)


# Resource definition
@ns.route("")
class ImportingResource(Resource):
    @ns.expect(parser)
    @ns.marshal_with(model, as_list=True, code=200)
    def get(self):
        # Parse query parameters
        args = parser.parse_args()
        year = args.get("year", 2024)
        country = args.get("country", None)

        # Create filter and service
        product_filter = Filter(country=country)
        service = get_importing_service()

        # Fetch and return products
        return service.get_all_products(year=year, product_filter=product_filter)
