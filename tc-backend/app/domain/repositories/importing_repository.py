from abc import ABC, abstractmethod


class ImportingRepository(ABC):
    @abstractmethod
    def fetch_all(self, year: int):
        pass
