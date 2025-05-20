from abc import abstractmethod, ABC
from typing import List

from app.models.category import Category
from app.models.exporting import Exporting
from app.models.importing import Importing
from app.models.product import Product
from app.models.processing import Processing


class UserRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str):
        """Get user by username"""
        pass


class ProductionRepository(ABC):
    @abstractmethod
    def fetch_by_year(self, year: int) -> List[Product]:
        """Get production data"""
        pass


class CommercializationRepository(ABC):
    @abstractmethod
    def fetch_by_year(self, year: int) -> List[Product]:
        """Get commercialization data"""
        pass


class ImportingRepository(ABC):
    @abstractmethod
    def fetch_categories(self) -> List[Category]:
        """Get categories"""
        pass

    @abstractmethod
    def fetch_imports_by_category_and_year(
        self, category_id: str, year: int
    ) -> List[Importing]:
        """Get imports by category and year"""
        pass


class ExportingRepository(ABC):
    @abstractmethod
    def fetch_categories(self) -> List[Category]:
        """Get categories"""
        pass

    @abstractmethod
    def fetch_imports_by_category_and_year(
        self, category_id: str, year: int
    ) -> List[Exporting]:
        """Get imports by category and year"""
        pass


class ProcessingRepository(ABC):
    @abstractmethod
    def fetch_categories(self) -> List[Category]:
        """Get categories"""
        pass

    @abstractmethod
    def fetch_process_by_category_and_year(
        self, category_id: str, year: int
    ) -> List[Processing]:
        """Get processing by category and year"""
        pass
