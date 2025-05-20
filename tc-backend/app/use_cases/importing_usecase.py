from typing import List

from app.interfaces.repository import ImportingRepository
from app.models.category import Category
from app.models.importing import Importing


class ImportingUseCase:
    def __init__(self, importing_repository: ImportingRepository):
        self.importing_repository = importing_repository

    def get_categories(
        self,
    ) -> List[Category]:
        return self.importing_repository.fetch_categories()

    def get_imports_by_category_and_year(
        self, category_id: str, year: int
    ) -> List[Importing]:
        return self.importing_repository.fetch_imports_by_category_and_year(
            category_id, year
        )
