from typing import List
from abc import ABC, abstractmethod
from app.domain.entities.category import Category


class ImportingRepository(ABC):
    @abstractmethod
    def fetch_all_categories(self) -> List[Category]:
        pass
    @abstractmethod
    def fetch_imports_by_category(self, start_year: int, end_year: int, category: str):
        pass
