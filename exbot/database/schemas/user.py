from typing import List

from pydantic import BaseModel, Field
from .excursion import ExcursionCreate, Excursion


class UserBase(BaseModel):
    telegram_id: int = Field(default=None)
    username: str
    phone: str


class UserCreate(UserBase):
    pass
    # excursions: List[ExcursionCreate] = Field(default=[])


class User(UserBase):
    id: int
    excursions: List[Excursion] = Field(default=[])

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "telegram_id": 411345345,
                "username": "Example",
                "email": "example@example.com",
            }
        }


class UserListResponse(BaseModel):
    users: List[User]
