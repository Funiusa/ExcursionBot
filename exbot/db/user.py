import datetime

from sqlalchemy import Column, Integer, VARCHAR, DATE, String, BigInteger, sql

# from db_utils import TimedBaseModel

from .base import BaseModel


# class User(TimedBaseModel):
#     __tablename__ = "users"
#     user_id = Column(BigInteger, primary_key=True)
#     name = Column(String(200), primary_key=True)
#     update_name = Column(String(50), primary_key=True)
#
#     query: sql.select


class User(BaseModel):
    __tablename__ = "users"
    user_id = Column(
        Integer, unique=True, nullable=False, primary_key=True
    )  # Telegram user id
    username = Column(VARCHAR(32), unique=False, nullable=True)

    registration_date = Column(DATE, default=datetime.date.today())
    update_date = Column(DATE, default=datetime.date.today())

    def __str__(self):
        return f"User: {self.user_id}"
