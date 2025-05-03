from typing import List
from app.domain.repositories.importing_repository import ImportingRepository
from app.domain.entities.category import Category


class ImportingService:
    def __init__(self, importing_repository: ImportingRepository):
        self.importing_repository = importing_repository

    def get_all_categories(self) -> List[Category]:
        # Fetch all categories from the repository
        categories = self.importing_repository.fetch_all_categories()
        return categories

    def get_imports_by_category(self, start_year: int, end_year: int, category: str):
        importing = self.importing_repository.fetch_imports_by_category(
            start_year=start_year,
            end_year=end_year,
            category=category
        )
        return importing
