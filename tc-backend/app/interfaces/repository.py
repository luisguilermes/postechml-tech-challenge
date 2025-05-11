from abc import abstractmethod, ABC
from typing import List

from app.models.product import Product


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
