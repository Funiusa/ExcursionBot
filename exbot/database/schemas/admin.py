from typing import Union
from pydantic import BaseModel, Field


class AdminBase(BaseModel):
    telegram_id: Union[int, None] = None
    username: str = Field(default=None)
    email: str = Field(default=None)


class AdminCreate(AdminBase):
    password: str = Field(default=None)

    class Config:
        orm_mode = True


class Admin(AdminBase):
    id: int
    password: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "telegram_id": 411345345,
                "username": "Example",
                "email": "example@example.com",
                "password": "pass",
            }
        }


class AdminLogin(BaseModel):
    username: str
    password: str
