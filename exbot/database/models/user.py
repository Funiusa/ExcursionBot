from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base
from .excursion import Excursion

from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    Table,
    ForeignKey,
    Boolean,
)

user_excursions = Table(
    "user_excursions",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("excursion_id", Integer, ForeignKey("excursions.id"), primary_key=True),
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
        "Excursion", secondary=user_excursions
    )

    def __str__(self):
        return f"User: {self.username}"
