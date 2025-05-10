from abc import abstractmethod, ABC
from typing import List

from app.domain.production import Production


class UserRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str):
        """Get user by username"""
        pass


class ProductionRepository(ABC):
    @abstractmethod
    def fetch_by_year(self, year: int) -> List[Production]:
        """Get production data"""
        pass
