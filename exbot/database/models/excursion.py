from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String,
    Boolean,
    Text,
)
from database.base import Base
from .question import Question


class Excursion(Base):
    __tablename__ = "excursions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    intro: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    image: Mapped[str] = mapped_column(String(100), nullable=True)

    questions: Mapped[List["Question"]] = relationship(
        "Question",
        back_populates="excursion",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __str__(self):
        return self.title

