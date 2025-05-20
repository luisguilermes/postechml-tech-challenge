from typing import List

from app.interfaces.repository import ProcessingRepository
from app.models.category import Category
from app.models.processing import Processing


class ProcessingUseCase:
    def __init__(self, processing_repository: ProcessingRepository):
        self.processing_repository = processing_repository

    def get_categories(
        self,
    ) -> List[Category]:
        return self.processing_repository.fetch_categories()

    def get_process_by_category_and_year(
        self, category_id: str, year: int
    ) -> List[Processing]:
        return self.processing_repository.fetch_process_by_category_and_year(
            category_id, year
        )
