from fastapi.responses import JSONResponse

from app.config.bindings import inject
from app.routers.router_wrapper import RouterWrapper
from app.services.auth.auth_service import AuthService
from app.services.user.user_service import UserService


class InfoRouter(RouterWrapper):
    @inject
    def __init__(self, user_service: UserService, auth_service: AuthService):
        super().__init__(prefix="/info")
        self.user_service = user_service
        self.auth_service = auth_service


    def _define_routes(self):
        @self.router.get("/is-initialized")
        def is_initialized():
            all_users = self.user_service.get_all()
            is_first = len(all_users) == 0
            return JSONResponse(content={"is_initialized": not is_first})
