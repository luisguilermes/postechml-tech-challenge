from abc import ABC, abstractmethod


class ProductionRepository(ABC):
    @abstractmethod
    def fetch_all(self, year: int):
        pass
