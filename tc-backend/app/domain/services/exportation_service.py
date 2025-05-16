from app.domain.repositories.base_repository import BaseRepository
from app.domain.vo.exportation_filter import ExportationFilter


class ExportationService:
    def __init__(self, exportation_repository: BaseRepository):
        self.exportation_repository = exportation_repository

    def get_all_products(self, year: int, exportation_filter: ExportationFilter = None):
        products = self.exportation_repository.fetch_all(year=year)
        if exportation_filter:
            products = exportation_filter.apply(products)
        return products
