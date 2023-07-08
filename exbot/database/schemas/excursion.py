from typing import List

from pydantic import BaseModel, Field

from .question import Question


class ExcursionBase(BaseModel):
    title: str
    intro: str
    description: str
    image: str
    is_published: bool = Field(default=False)


class ExcursionCreate(ExcursionBase):
    pass


class Excursion(ExcursionBase):
    id: int
    questions: List[Question] = Field(default=[])

    class Config:
        orm_mode = True


class UserExcursions(ExcursionBase):
    id: int

    class Config:
        orm_mode = True
