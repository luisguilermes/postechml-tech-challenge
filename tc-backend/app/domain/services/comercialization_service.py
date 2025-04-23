from app.domain.repositories.comercialization_repository import ComercializationRepository
from app.domain.vo.product_filter import Filter


class ComercializationService:
    def __init__(self, comercialization_repository: ComercializationRepository):
        self.comercialization_repository = comercialization_repository

    def get_all_products(self, year: int, product_filter: Filter = None):
        products = self.comercialization_repository.fetch_all(year=year)
        if product_filter:
            products = product_filter.apply(products)
        return products
