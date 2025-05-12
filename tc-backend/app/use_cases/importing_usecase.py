from typing import List

from app.interfaces.repository import ImportingRepository
from app.models.category import Category


class ImportingUseCase:
    def __init__(self, importing_repository: ImportingRepository):
        self.importing_repository = importing_repository

    def get_categories(
        self,
    ) -> List[Category]:
        return self.importing_repository.fetch_categories()
