from flask_restx import Namespace, Resource, fields, reqparse
from app.adapters.repositories.scrapers.production_embrapa_scraper import (
    ProductionEmbrapaScraper,
)
from app.domain.services.production_service import ProductionService
from app.domain.vo.product_filter import Filter


ns = Namespace(
    "production",
    description="Produção de vinhos, sucos e derivados do Rio Grande do Sul",
)

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
parser = reqparse.RequestParser()
parser.add_argument("category", type=str, required=False, help="Filter by category")
parser.add_argument(
    "year", type=int, required=False, help="Filter by year", default=2023
)


@ns.route("")
class ProductResource(Resource):
    @ns.expect(parser)
    @ns.marshal_with(model, as_list=True, code=200)
    def get(self):
        args = parser.parse_args()
        year = args.get("year")
        category = args.get("category")
        product_filter = Filter(category=category)

        repo = ProductionEmbrapaScraper()
        service = ProductionService(repo)
        products = service.get_all_products(year=year, product_filter=product_filter)

        return products
