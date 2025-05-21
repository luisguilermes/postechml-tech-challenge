from typing import List

from app.interfaces.repository import ExportingRepository
from app.models.category import Category
from app.models.exporting import Exporting


class ExportingUseCase:
    def __init__(self, exporting_repository: ExportingRepository):
        self.exporting_repository = exporting_repository

    def get_categories(
        self,
    ) -> List[Category]:
        return self.exporting_repository.fetch_categories()

    def get_exporting_by_category_and_year(
        self, category_id: str, year: int
    ) -> List[Exporting]:
        return self.exporting_repository.fetch_imports_by_category_and_year(
            category_id, year
        )
