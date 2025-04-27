from flask_restx import Namespace, Resource, fields, reqparse
from app.domain.vo.product_filter import Filter
from app.adapters.repositories.scrapers.processing_embrapa_scraper import ProcessingEmbrapaScraper
from app.adapters.repositories.scrapers.production_embrapa_scraper import ProductionEmbrapaScraper
from app.domain.services.processing_service import ProcessingService
from app.domain.services.production_service import ProductionService

model_fields = {
    "id": fields.String,
    "amount": fields.Float,
    "unit": fields.String,
    "category": fields.String,
    "sub_category": fields.String,
    "source": fields.String,
    "collected_at": fields.DateTime,
    "year": fields.Integer,
}

parser = reqparse.RequestParser()
parser.add_argument("category", type=str, required=False, help="Filter by category")
parser.add_argument("year", type=int, required=False, help="Filter by year", default=2023)

# Factory function to create the service
def get_production_service():
    return ProductionService(ProductionEmbrapaScraper())

# Factory function to create the service
def get_processing_service():
    return ProcessingService(ProcessingEmbrapaScraper())

def register_product_resource(namespace_name, description, service_factory):
    ns = Namespace(namespace_name, description=description)
    model = ns.model("Model", model_fields)

    @ns.route("")
    class BaseProductResource(Resource):
        @ns.expect(parser)
        @ns.marshal_with(model, as_list=True, code=200)
        def get(self):
            args = parser.parse_args()
            year = args.get("year", 2023)
            category = args.get("category", None)
            product_filter = Filter(category=category)
            service = service_factory()
            return service.get_all_products(year=year, product_filter=product_filter)

    return ns
