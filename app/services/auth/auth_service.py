from abc import ABC, abstractmethod

from app.models.user import User


class AuthService(ABC):
    @abstractmethod
    def login(self, username: str, password: str, rememberme: bool):
        pass

    @abstractmethod
    def get_validated_user_from_credentials(self, username: str, password: str) -> User:
        pass

    @abstractmethod
    def get_validated_user_from_token(self, token: str) -> User:
        pass

    @abstractmethod
    def get_validated_user_from_token_and_pin(self, token: str, pin: str) -> User:
        pass

    @abstractmethod
    def get_pwd_context(self):
        pass

    @abstractmethod
    def get_permissions(self):
        pass
