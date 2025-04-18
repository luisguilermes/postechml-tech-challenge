from abc import ABC, abstractmethod


class ProcessingRepository(ABC):
    @abstractmethod
    def fetch_all(self, year: int):
        pass
