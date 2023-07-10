from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    place: Mapped[str] = mapped_column(nullable=True)
    answer: Mapped[str] = mapped_column(nullable=False)
    hint: Mapped[str] = mapped_column(nullable=True)
    text: Mapped[str] = mapped_column(nullable=False)
    correct: Mapped[str] = mapped_column(nullable=False)
    addition: Mapped[str] = mapped_column(nullable=True)
    final: Mapped[str] = mapped_column(nullable=False)

    excursion_id: Mapped[int] = mapped_column(
        ForeignKey("excursions.id", ondelete="CASCADE")
    )
    excursion = relationship("Excursion", back_populates="questions")
