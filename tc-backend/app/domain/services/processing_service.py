from app.domain.repositories.base_repository import BaseRepository
from app.domain.vo.product_filter import Filter


class ProcessingService:
    def __init__(self, processing_repository: BaseRepository):
        self.processing_repository = processing_repository

    def get_all_products(self, year: int, suboption: str, product_filter: Filter = None):
        products = self.processing_repository.fetch_all(year=year, suboption=suboption)
        if product_filter:
            products = product_filter.apply(products)
        return products
