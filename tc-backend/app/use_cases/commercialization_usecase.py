from typing import List

from app.models.product import Product
from app.interfaces.repository import CommercializationRepository


class CommercializationUseCase:
    def __init__(self, commercialization_repository: CommercializationRepository):
        self.commercialization_repository = commercialization_repository

    def get_production_by_year(
        self,
        year: int = 2023,
    ) -> List[Product]:
        return self.commercialization_repository.fetch_by_year(year)
