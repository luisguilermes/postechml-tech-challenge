from abc import ABC, abstractmethod


class UserRepository(ABC):
    @abstractmethod
    def find_by_username(self, username: str): pass

    @abstractmethod
    def save(self, username: str, password_hash: str): pass