from typing import List

from app.models.product import Product
from app.interfaces.repository import ProductionRepository


class ProductionUseCase:
    def __init__(self, production_repository: ProductionRepository):
        self.production_repository = production_repository

    def get_production_by_year(
        self,
        year: int = 2023,
    ) -> List[Product]:
        return self.production_repository.fetch_by_year(year)
