from pydantic import BaseModel, Field


class QuestionBase(BaseModel):
    place: str
    answer: str
    hint: str
    text: str
    correct: str
    addition: str
    final: str


class QuestionCreate(QuestionBase):
    pass


class Question(QuestionBase):
    id: int
    excursion_id: int

    class Config:
        orm_mode = True
