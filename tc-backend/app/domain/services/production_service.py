from app.domain.repositories.base_repository import BaseRepository
from app.domain.vo.product_filter import Filter


class ProductionService:
    def __init__(self, production_repository: BaseRepository):
        self.production_repository = production_repository

    def get_all_products(self, year: int, product_filter: Filter = None):
        products = self.production_repository.fetch_all(year=year)
        if product_filter:
            products = product_filter.apply(products)
        return products
