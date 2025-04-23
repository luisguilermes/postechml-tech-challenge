from abc import ABC, abstractmethod


class ComercializationRepository(ABC):
    @abstractmethod
    def fetch_all(self, year: int):
        pass
