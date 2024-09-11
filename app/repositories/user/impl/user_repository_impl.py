from typing import Sequence

from sqlmodel import select

from app.database.database_connector import DatabaseConnector
from app.exceptions.bad_request_exception import BadRequestException
from app.exceptions.not_found_exception import NotFoundException
from app.models.user import User
from app.repositories.user.user_repository import UserRepository


class UserRepositoryImpl(UserRepository):
    def __init__(self, database_connector: DatabaseConnector):
        self.database_connector = database_connector


    def find_by_id(self, user_id: int) -> User:
        statement = select(User).where(User.id == user_id)
        user_db = self.database_connector.get_session().exec(statement).first()
        if user_db is None:
            raise NotFoundException("User was not found")

        return user_db


    def find_by_email(self, email: str) -> User:
        statement = select(User).where(User.email == email)
        user_db = self.database_connector.get_session().exec(statement).first()
        if user_db is None:
            raise NotFoundException("User was not found")

        return user_db


    def create(self, user: User) -> User:
        try:
            self.find_by_id(user.user_id)
        except NotFoundException:
            self.database_connector.get_session().add(user)
            self.database_connector.get_session().commit()
            self.database_connector.get_session().refresh(user)
            return user
        raise BadRequestException("User already exists")


    def update(self, user: User) -> User:
        user_db = self.find_by_id(user.id)
        user_db.email = user.email
        user_db.password = user.password
        self.database_connector.get_session().commit()
        self.database_connector.get_session().refresh(user_db)
        return user_db


    def delete_by_id(self, user_id: int) -> User:
        user_db = self.find_by_id(user_id)
        self.database_connector.get_session().delete(user_db)
        self.database_connector.get_session().commit()
        return user_db


    def find_all(self) -> Sequence[User]:
        statement = select(User)
        return self.database_connector.get_session().exec(statement).all()
