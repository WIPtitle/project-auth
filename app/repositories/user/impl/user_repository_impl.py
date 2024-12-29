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
        session = self.database_connector.get_new_session()
        user_db = session.exec(statement).first()
        session.close()
        if user_db is None:
            raise NotFoundException("User was not found")

        return user_db


    def find_by_email(self, email: str) -> User:
        statement = select(User).where(User.email == email)
        session = self.database_connector.get_new_session()
        user_db = session.exec(statement).first()
        session.close()
        if user_db is None:
            raise NotFoundException("User was not found")

        return user_db


    def create(self, user: User) -> User:
        try:
            self.find_by_email(user.email)
        except NotFoundException:
            session = self.database_connector.get_new_session()
            session.add(user)
            session.commit()
            session.refresh(user)
            session.close()
            return user
        raise BadRequestException("User already exists")


    def update(self, user: User) -> User:
        statement = select(User).where(User.id == user.id)
        session = self.database_connector.get_new_session()
        user_db = session.exec(statement).first()
        if user_db is None:
            raise NotFoundException("User was not found")

        user_db.email = user.email
        if user.password is not None and user.password != "":
            user_db.password = user.password
        if user.pin is not None and user.pin != "":
            user_db.pin = user.pin
        user_db.permissions = user.permissions
        session.commit()
        session.refresh(user_db)
        session.close()
        return user_db


    def delete_by_id(self, user_id: int) -> User:
        statement = select(User).where(User.id == user_id)
        session = self.database_connector.get_new_session()
        user_db = session.exec(statement).first()
        if user_db is None:
            raise NotFoundException("User was not found")

        session.delete(user_db)
        session.commit()
        session.close()
        return user_db


    def find_all(self) -> Sequence[User]:
        statement = select(User)
        session = self.database_connector.get_new_session()
        result = session.exec(statement).all()
        session.close()
        return result
