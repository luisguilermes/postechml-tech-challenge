from abc import ABC, abstractmethod


class BaseRepository(ABC):
    @abstractmethod
    def fetch_all(self, year: int, suboption: str):
        pass
