from flask_restx import Namespace, Resource, fields, reqparse
from app.adapters.repositories.scrapers.Exportation_embrapa_escraper import (
    ExportationEmbrapaScraper,
)
from app.domain.services.exportation_service import ExportationService
from app.domain.vo.exportation_filter import ExportationFilter


# Namespace definition
ns = Namespace(
    "Exportation",
    description="Comercialização de vinhos, sucos e derivados do Rio Grande do Sul",
)

# Model definition for API response
model = ns.model(
    "ExportationModel",
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
def get_exportation_service():
    repo = ExportationEmbrapaScraper()
    return ExportationService(repo)


# Resource definition
@ns.route("")
class ExportationResource(Resource):
    @ns.expect(parser)
    @ns.marshal_with(model, as_list=True, code=200)
    def get(self):
        # Parse query parameters
        args = parser.parse_args()
        year = args.get("year", 2023)
        category = args.get("category", None)

        # Create filter and service
        product_filter = ExportationFilter(category=category)
        service = get_exportation_service()

        # Fetch and return products
        return service.get_all_products(year=year, product_filter=product_filter)
