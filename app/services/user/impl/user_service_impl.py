from typing import Sequence

from app.exceptions.unupdateable_data_exception import UnupdateableDataException
from app.models.user import User
from app.repositories.user.user_repository import UserRepository
from app.services.user.user_service import UserService


class UserServiceImpl(UserService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository


    def get_by_id(self, user_id: int) -> User:
        return self.user_repository.find_by_id(user_id)


    def get_by_email(self, email: str) -> User:
        return self.user_repository.find_by_email(email)


    def create(self, user: User) -> User:
        user = self.user_repository.create(user)
        return user


    def update(self, user_id: int, user: User) -> User:
        # User has id null since it comes from dto without id. Even if service gets used elsewhere,
        # user.id should always match user_id.
        user.id = user_id
        user = self.user_repository.update(user)
        return user


    def delete_by_id(self, user_id: int) -> User:
        user = self.user_repository.delete_by_id(user_id)
        return user


    def get_all(self) -> Sequence[User]:
        return self.user_repository.find_all()

