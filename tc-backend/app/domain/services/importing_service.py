from app.domain.repositories.importing_repository import ImportingRepository
from app.domain.vo.product2_filter import Filter


class ImportingService:
    def __init__(self, importing_repository: ImportingRepository):
        self.importing_repository = importing_repository

    def get_all_products(self, year: int, product_filter: Filter = None):
        #products = self.importing_repository.fetch_all(year=year)
        products = self.importing_repository.fetch_all(start_year=year, end_year=year)
        if product_filter:
            products = product_filter.apply(products)
        return products
