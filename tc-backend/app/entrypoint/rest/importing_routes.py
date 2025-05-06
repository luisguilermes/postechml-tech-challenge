from flask_restx import Namespace, Resource, fields, reqparse
from app.adapters.repositories.scrapers.importing_embrapa_scraper import (
    ImportingEmbrapaScraper,
)
from app.domain.services.importing_service import ImportingService
from app.domain.vo.importing_filter import ImportingFilter

# Namespace definition
ns = Namespace(
    "importing",
    description="Importação de vinhos, sucos e derivados do Rio Grande do Sul",
)

# Model definition for API response
category_model = ns.model(
    "CategoryModel",
    {
        "id": fields.String,
        "name": fields.String,
        "source": fields.String,
        "collected_at": fields.DateTime,
    },
)

model = ns.model(
    "ImportingModel",
    {
        "category": fields.String,
        "country": fields.String,
        "amount": fields.Float,
        "amount_unit": fields.String,
        "value": fields.Float,
        "value_unit": fields.String,
        "source": fields.String,
        "collected_at": fields.DateTime,
        "year": fields.Integer,
    },
)

# Request parser for query parameters
parser = reqparse.RequestParser()
parser.add_argument(
"start_year", type=int, required=False, help="Filter by start_year", default=2024
)
parser.add_argument(
    "end_year", type=int, required=False, help="Filter by end_year", default=2024
)
parser.add_argument(
    "country", type=str, required=False, help="Filter by country", default=None
)


# Factory function to create the service
def get_importing_service():
    repo = ImportingEmbrapaScraper()
    return ImportingService(repo)


# Resource definition
@ns.route("/categories")
class CategoriesResource(Resource):
    @ns.marshal_with(category_model, as_list=True, code=200)
    def get(self):
        service = get_importing_service()
        # Fetch and return products
        return service.get_all_categories()


@ns.route("/categories/<string:category_id>")
class CategoryResource(Resource):
    @ns.expect(parser)
    @ns.marshal_with(model, code=200)
    def get(self, category_id: str):
        # Parse query parameters
        args = parser.parse_args()
        country = args.get("country", None)
        start_year = args.get("start_year", 2024)
        end_year = args.get("end_year", 2024)

        # Create filter and service
        importing_filter = ImportingFilter(country=country)
        service = get_importing_service()

        # Fetch and return products for the specific category
        return service.get_imports_by_category(
            category=category_id,
            start_year=start_year,
            end_year=end_year,
            importing_filter=importing_filter,
        )
