from fastapi import Depends

from app.config.bindings import inject
from app.exceptions.authentication_exception import AuthenticationException
from app.models.user import User, UserInputDto
from app.routers.impl.auth_router import oauth2_scheme
from app.routers.router_wrapper import RouterWrapper
from app.services.auth.auth_service import AuthService
from app.services.user.user_service import UserService


class UserRouter(RouterWrapper):
    @inject
    def __init__(self, user_service: UserService, auth_service: AuthService):
        super().__init__(prefix="/user")
        self.user_service = user_service
        self.auth_service = auth_service


    def _define_routes(self):
        @self.router.post("/")
        def create_user(user: UserInputDto):
            user.password = self.auth_service.get_pwd_context().hash(user.password)
            return User.to_response(self.user_service.create(User.from_dto(user)))


        @self.router.get("/{user_id}")
        def get_user(user_id: int):
            return User.to_response(self.user_service.get_by_id(user_id))


        @self.router.put("/{user_id}")
        def update_user(user_id: int, user: UserInputDto, token: str = Depends(oauth2_scheme)):
            token_user = self.auth_service.get_validated_user_from_token(token)
            if token_user.id != user_id:
                raise AuthenticationException("Can't update a user that is not yourself")

            user.password = self.auth_service.get_pwd_context().hash(user.password)
            return User.to_response(self.user_service.update(user_id, User.from_dto(user)))


        @self.router.delete("/{user_id}")
        def delete_user(user_id: int, token: str = Depends(oauth2_scheme)):
            token_user = self.auth_service.get_validated_user_from_token(token)
            if token_user.id != user_id:
                raise AuthenticationException("Can't delete a user that is not yourself")

            return User.to_response(self.user_service.delete_by_id(user_id))
