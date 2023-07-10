from typing import Optional, List

from pydantic import BaseModel, Field


class QuestionBase(BaseModel):
    place: Optional[str]
    answer: str
    hint: str
    text: Optional[str]
    correct: str
    addition: Optional[str] = Field(default=None)
    final: str


class QuestionCreate(QuestionBase):
    id: int


class Question(QuestionBase):
    id: int
    excursion_id: int

    class Config:
        orm_mode = True
