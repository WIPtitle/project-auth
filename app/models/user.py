from pydantic import EmailStr
from sqlmodel import SQLModel, Field


class UserInputDto(SQLModel):
    email: EmailStr
    password: str

class UserResponse(SQLModel):
    id: int
    email: str

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True)
    password: str

    @classmethod
    def from_dto(cls, dto: UserInputDto):
        return cls(
            id=None,
            email=dto.email,
            password=dto.password
        )

    def to_response(self):
        return UserResponse(id=self.id, email=self.email)