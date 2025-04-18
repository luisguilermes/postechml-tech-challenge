from app.domain.repositories.processing_repository import ProcessingRepository
from app.domain.vo.product_filter import Filter


class ProcessingService:
    def __init__(self, processing_repository: ProcessingRepository):
        self.processing_repository = processing_repository

    def get_all_products(self, year: int, product_filter: Filter = None):
        products = self.processing_repository.fetch_all(year=year)
        if product_filter:
            products = product_filter.apply(products)
        return products
