from flask_restx import Namespace, Resource, fields, reqparse
from app.adapters.repositories.scrapers.processing_embrapa_scraper import (
    ProcessingEmbrapaScraper,
)
from app.domain.services.processing_service import ProcessingService
from app.domain.vo.product_filter import Filter


# Namespace definition
ns = Namespace(
    "processing",
    description="Processamento de vinhos, sucos e derivados do Rio Grande do Sul",
)

# Model definition for API response
model = ns.model(
    "ProcessingModel",
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


sub_option = {
    'Viníferas': 'subopt_01',
    'Americanas e híbridas': 'subopt_02',
    'Uvas de mesa': 'subopt_03',
    'Sem classificação': 'subopt_04'
}


# Request parser for query parameters
parser = reqparse.RequestParser()
# parser.add_argument("category", type=str, required=False, help="Filter by category")
parser.add_argument("suboption", type=str, choices=list(sub_option.keys()),
                    required=False, default='Viníferas',
                    help="Escolha uma subopção para filtrar os resultados.")
parser.add_argument(
    "year",
    type=int,
    required=False,
    default=2023,
    choices=list(range(1970, 2024)),
    help="Escolha entre os anos 1970 e 2023."
)


# Factory function to create the service
def get_processing_service():
    repo = ProcessingEmbrapaScraper()
    return ProcessingService(repo)


# Resource definition
@ns.route("")
class ProcessingResource(Resource):
    @ns.expect(parser)
    @ns.marshal_with(model, as_list=True, code=200)
    def get(self):
        # Parse query parameters
        args = parser.parse_args()
        year = args.get("year", 2023)
        sub_amigavel = args.get("suboption")
        suboption = sub_option.get(sub_amigavel)
        #category = args.get("category", None)

        # Create filter and service
        product_filter = Filter()
        service = get_processing_service()

        # Fetch and return products
        #return service.get_all_products(year=year, product_filter=product_filter)
        return service.get_all_products(year=year,
                                        suboption=suboption,
                                        product_filter=product_filter)
