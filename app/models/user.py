from typing import List

from pydantic import EmailStr
from sqlalchemy import Column
from sqlmodel import SQLModel, Field

from app.models.enum.permission import Permission, PermissionList


class UserInputDto(SQLModel):
    email: EmailStr
    password: str
    pin: str
    permissions: List[Permission]
    password_check: str | None = None

class UserResponse(SQLModel):
    id: int
    email: str
    permissions: List[Permission]

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True)
    password: str
    pin: str
    permissions: List[Permission] = Field(sa_column=Column(PermissionList))

    @classmethod
    def from_dto(cls, dto: UserInputDto):
        return cls(
            id=None,
            email=dto.email,
            password=dto.password,
            pin=dto.pin,
            permissions=dto.permissions
        )

    def to_response(self):
        return UserResponse(id=self.id, email=self.email, permissions=self.permissions)