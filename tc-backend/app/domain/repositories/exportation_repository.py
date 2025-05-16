from typing import List
from abc import ABC, abstractmethod
from app.domain.entities.exportation import Exportation


class ExportationRepository(ABC):
    @abstractmethod
    def fetch_all_categories(self) -> List[Exportation]:
        pass
    @abstractmethod
    def fetch_exportation_by_category(self, start_year: int, end_year: int, category: str):
        pass
