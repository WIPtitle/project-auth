from enum import Enum

from sqlalchemy import TypeDecorator, VARCHAR


class Permission(str, Enum):
    USER_MANAGER = "USER_MANAGER",
    START_ALARM = "START_ALARM",
    STOP_ALARM = "STOP_ALARM",
    ACCESS_RECORDINGS = "ACCESS_RECORDINGS",
    ACCESS_CAMERAS = "ACCESS_CAMERAS",
    CHANGE_ALARM_SOUND = "CHANGE_ALARM_SOUND"


class PermissionList(TypeDecorator):
    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return ','.join([perm.value for perm in value])

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return [Permission(perm) for perm in value.split(',')]