import os
from datetime import timedelta, datetime

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from app.config.bindings import inject
from app.exceptions.authentication_exception import AuthenticationException
from app.models.user import User, UserInputDto
from app.routers.router_wrapper import RouterWrapper
from app.services.user.user_service import UserService
from app.utils.read_credentials import read_credentials

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")

class UserRouter(RouterWrapper):
    @inject
    def __init__(self, user_service: UserService):
        super().__init__(prefix="/user")
        self.user_service = user_service

        secret_key_file = os.getenv('AUTH_SECRET_KEY_FILE')
        credentials = read_credentials(secret_key_file)
        self.secret_key = credentials['SECRET_KEY']

        self._define_routes()


    def _define_routes(self):
        @self.router.post("/create")
        def create_user(user: UserInputDto):
            user.password = pwd_context.hash(user.password)
            return User.to_response(self.user_service.create(User.from_dto(user)))


        @self.router.post("/token")
        def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
            user = authenticate_user(self.user_service, form_data.username, form_data.password)

            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                secret_key=self.secret_key, data={"sub": user.email}, expires_delta=access_token_expires
            )
            return {"access_token": access_token, "token_type": "bearer"}


        @self.router.get("/me")
        def read_users_me(token: str = Depends(oauth2_scheme)):
            return User.to_response(get_current_user(self.secret_key, self.user_service, token))


def authenticate_user(user_service: UserService, email: str, password: str):
    user = user_service.get_by_email(email)
    if not user or not pwd_context.verify(password, user.password):
        raise AuthenticationException("Wrong password")
    return user


def create_access_token(secret_key: str, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(secret_key: str, user_service: UserService, token: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise AuthenticationException("Malformed token")
    except Exception:
        raise AuthenticationException("JWT error")
    user = user_service.get_by_email(user_email)
    if user is None:
        raise AuthenticationException("User relative to this token doesn't exist")
    return user