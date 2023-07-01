from database.base import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import String, ForeignKey


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    place: Mapped[str] = mapped_column(String, nullable=True)
    answer: Mapped[str] = mapped_column(String(50), nullable=False)
    hint: Mapped[str] = mapped_column(String, nullable=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    correct: Mapped[str] = mapped_column(String, nullable=False)
    addition: Mapped[str] = mapped_column(String, nullable=False)
    final: Mapped[str] = mapped_column(String(100), nullable=False)

    excursion_id: Mapped[int] = mapped_column(ForeignKey("excursions.id"))
    excursion = relationship("Excursion", back_populates="questions")
