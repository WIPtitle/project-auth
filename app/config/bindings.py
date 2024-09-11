from functools import wraps
from typing import Callable, get_type_hints

from app.database.database_connector import DatabaseConnector
from app.database.impl.database_connector_impl import DatabaseConnectorImpl
from app.repositories.user.impl.user_repository_impl import UserRepositoryImpl
from app.repositories.user.user_repository import UserRepository
from app.services.user.impl.user_service_impl import UserServiceImpl
from app.services.user.user_service import UserService

bindings = { }

# Create instances only one time
database_connector = DatabaseConnectorImpl()


user_repository = UserRepositoryImpl(database_connector=database_connector)
user_service = UserServiceImpl(user_repository=user_repository)

# Put them in an interface -> instance dict so they will be used everytime a dependency is required
bindings[DatabaseConnector] = database_connector

bindings[UserRepository] = user_repository
bindings[UserService] = user_service


def resolve(interface):
    implementation = bindings[interface]
    if implementation is None:
        raise ValueError(f"No binding found for {interface}")
    return implementation


def inject(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        type_hints = get_type_hints(func)
        for name, param_type in type_hints.items():
            if param_type in bindings:
                kwargs[name] = resolve(param_type)
        return func(*args, **kwargs)
    return wrapper