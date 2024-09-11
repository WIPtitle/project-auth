from abc import ABC, abstractmethod
from typing import Sequence

from app.models.user import User


class UserService(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def update(self, user_id: int, user: User) -> User:
        pass

    @abstractmethod
    def delete_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def get_all(self) -> Sequence[User]:
        pass
