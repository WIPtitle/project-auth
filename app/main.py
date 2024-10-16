from typing import List

from fastapi import FastAPI

from app.config.handlers import get_exception_handlers
from app.routers.impl.auth_router import AuthRouter
from app.routers.impl.user_router import UserRouter
from app.routers.impl.info_router import InfoRouter
from app.routers.router_wrapper import RouterWrapper

exception_handlers = get_exception_handlers()
routers: List[RouterWrapper] = [
    AuthRouter(),
    UserRouter(),
    InfoRouter()
]

app = FastAPI()

for exc, handler in exception_handlers:
    app.add_exception_handler(exc, handler)

for router in routers:
    app.include_router(router.get_fastapi_router())
