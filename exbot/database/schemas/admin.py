import pydantic
from pydantic import BaseModel


class AdminBase(BaseModel):
    telegram_id: int = pydantic.Field(default=None)
    username: str = pydantic.Field(default=None)
    email: str = pydantic.Field(default=None)


class AdminCreate(AdminBase):
    password: str = pydantic.Field(default=None)

    class Config:
        the_schema = {
            "admin_demo": {
                "telegram_id": 2345345,
                "username": "admin",
                "email": "admin@admin.com",
                "password": "adminpassword134",
            }
        }


class Admin(AdminBase):
    id: int
    telegram_id: int = pydantic.Field(default=None)
    username: str = pydantic.Field(default=None)
    email: str = pydantic.Field(default=None)
    is_superuser: bool = pydantic.Field(default=False)

    class Config:
        orm_mode = True


class AdminLogin(BaseModel):
    email: str = pydantic.Field(default=None)
    password: str = pydantic.Field(default=None)

    class Config:
        the_schema = {
            "admin_demo_login": {
                "email": "admin@admin.com",
                "password": "adminpassword134",
            }
        }
