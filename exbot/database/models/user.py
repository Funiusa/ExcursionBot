from typing import List, Optional

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import BigInteger

from database.base import Base

from .excursion import Excursion

user_excursions = Table(
    "user_excursions",
    Base.metadata,
    Column(
        "user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "excursion_id",
        Integer,
        ForeignKey("excursions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    telegram_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, nullable=False, index=True
    )
    username: Mapped[Optional[str]]
    phone: Mapped[str] = Column(String, unique=True, nullable=False)
    excursions: Mapped[List["Excursion"]] = relationship(
        "Excursion",
        secondary=user_excursions,
        cascade="all, delete",
    )

    def __str__(self):
        return f"User: {self.username}"
