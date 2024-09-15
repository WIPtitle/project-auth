from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.config.bindings import inject
from app.models.user import User
from app.routers.router_wrapper import RouterWrapper
from app.services.auth.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

class AuthRouter(RouterWrapper):
    @inject
    def __init__(self, auth_service: AuthService):
        super().__init__(prefix="/auth")
        self.auth_service = auth_service


    def _define_routes(self):
        @self.router.post("/token")
        def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
            return self.auth_service.login(form_data.username, form_data.password)


        @self.router.get("/user")
        def read_users_me(token: str = Depends(oauth2_scheme)):
            return User.to_response(self.auth_service.get_validated_user_from_token(token))


        @self.router.get("/permissions")
        def get_all_permissions():
            return self.auth_service.get_permissions()
