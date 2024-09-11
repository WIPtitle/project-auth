from fastapi import Depends

from app.config.bindings import inject
from app.exceptions.authentication_exception import AuthenticationException
from app.exceptions.bad_request_exception import BadRequestException
from app.exceptions.permission_exception import PermissionException
from app.models.enum.permission import Permission
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
        @self.router.post("/first", operation_id="create_non_auth_user")
        def create_user(user: UserInputDto):
            # First user gets to pass every permission that he wants, it gets overwritten by all permissions
            if len(self.user_service.get_all()) == 0:
                user.password = self.auth_service.get_pwd_context().hash(user.password)
                user.permissions = [permission for permission in Permission]
                return User.to_response(self.user_service.create(User.from_dto(user)))
            else:
                raise BadRequestException("First user has already been created")


        @self.router.post("/")
        def create_user_authenticated(user: UserInputDto, token: str = Depends(oauth2_scheme)):
            token_user = self.auth_service.get_validated_user_from_token(token)
            if Permission.USER_MANAGER in token_user.permissions:
                user.password = self.auth_service.get_pwd_context().hash(user.password)
                return User.to_response(self.user_service.create(User.from_dto(user)))
            else:
                raise PermissionException("You don't have permission to create a new account")


        @self.router.get("/{user_id}")
        def get_user(user_id: int):
            return User.to_response(self.user_service.get_by_id(user_id))


        @self.router.put("/{user_id}")
        def update_user(user_id: int, user: UserInputDto, token: str = Depends(oauth2_scheme)):
            token_user = self.auth_service.get_validated_user_from_token(token)

            if Permission.USER_MANAGER not in token_user.permissions:
                if token_user.id != user_id:
                    raise AuthenticationException("Can't update a user that is not yourself")

                if set(token_user.permissions) != set(user.permissions):
                    raise PermissionException("Can't update your permissions unless user manager")

            user.password = self.auth_service.get_pwd_context().hash(user.password)
            return User.to_response(self.user_service.update(user_id, User.from_dto(user)))


        @self.router.delete("/{user_id}")
        def delete_user(user_id: int, token: str = Depends(oauth2_scheme)):
            token_user = self.auth_service.get_validated_user_from_token(token)
            if Permission.USER_MANAGER not in token_user.permissions:
                if token_user.id != user_id:
                    raise AuthenticationException("Can't delete a user that is not yourself")

            return User.to_response(self.user_service.delete_by_id(user_id))
