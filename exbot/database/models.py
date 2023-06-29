from database.base import Base, SessionLocal
from typing import Optional, List
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Column, Integer, String, Table, ForeignKey, MetaData, Boolean, Text

meta = MetaData()

user_excursions = Table(
    "user_excursions",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("excursion_id", Integer, ForeignKey("excursions.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(unique=True, nullable=False, index=True)
    username: Mapped[Optional[str]]
    phone: Mapped[str] = Column(String, unique=True, nullable=False)

    excursions: Mapped[List["Excursion"]] = relationship(
        "Excursion", secondary=user_excursions
    )

    def __str__(self):
        return f"User: {self.username}"


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
        "Question", back_populates="excursion", cascade="all, delete-orphan",
        passive_deletes=True
    )

    def __str__(self):
        return self.title


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
