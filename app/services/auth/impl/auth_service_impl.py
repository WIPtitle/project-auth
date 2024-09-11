import os
from datetime import timedelta, datetime

import jwt
from passlib.context import CryptContext

from app.exceptions.authentication_exception import AuthenticationException
from app.models.user import User
from app.repositories.user.user_repository import UserRepository
from app.services.auth.auth_service import AuthService
from app.utils.read_credentials import read_credentials


class AuthServiceImpl(AuthService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

        secret_key_file = os.getenv('AUTH_SECRET_KEY_FILE')
        credentials = read_credentials(secret_key_file)
        self.secret_key = credentials['SECRET_KEY']

        self.algorithm = "HS256"
        self.expiration = 30

        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


    def create_jwt_token(self, secret_key: str, data: dict, algorithm: str):
        to_encode = data.copy()
        expires_delta = timedelta(minutes=self.expiration)
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
        return encoded_jwt


    def login(self, email: str, password: str):
        user = self.get_validated_user_from_credentials(email, password)
        access_token = self.create_jwt_token(secret_key=self.secret_key, data={"sub": user.email}, algorithm=self.algorithm)
        return {"access_token": access_token, "token_type": "bearer"}


    def get_validated_user_from_credentials(self, email: str, password: str) -> User:
        user = self.user_repository.find_by_email(email)
        if not user or not self.pwd_context.verify(password, user.password):
            raise AuthenticationException("Wrong password")
        return user


    def get_validated_user_from_token(self, token: str) -> User:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_email: str = payload.get("sub")
            if user_email is None:
                raise AuthenticationException("Malformed token")
        except Exception:
            raise AuthenticationException("JWT error")
        user = self.user_repository.find_by_email(user_email)
        if user is None:
            raise AuthenticationException("User relative to this token doesn't exist")
        return user


    def get_pwd_context(self):
        return self.pwd_context
