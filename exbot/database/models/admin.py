from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base

import passlib.hash as _hash


class Admin(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    telegram_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, nullable=True, index=True
    )
    username: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=True, index=True)
    password: Mapped[str]

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.password)
