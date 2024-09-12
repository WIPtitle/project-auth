from abc import ABC, abstractmethod

from app.models.user import User


class AuthService(ABC):
    @abstractmethod
    def login(self, email: str, password: str):
        pass

    @abstractmethod
    def get_validated_user_from_credentials(self, email: str, password: str) -> User:
        pass

    @abstractmethod
    def get_validated_user_from_token(self, token: str) -> User:
        pass

    @abstractmethod
    def get_pwd_context(self):
        pass

    @abstractmethod
    def get_permissions(self):
        pass
