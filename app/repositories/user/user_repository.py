from abc import ABC, abstractmethod
from typing import Sequence

from app.models.user import User


class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        pass

    @abstractmethod
    def delete_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def find_all(self) -> Sequence[User]:
        pass
