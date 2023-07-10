from typing import List, Optional

from pydantic import BaseModel, Field, FilePath

from .question import Question


class ExcursionBase(BaseModel):
    title: str
    intro: str
    description: str
    is_published: bool = Field(default=False)


class ExcursionCreate(ExcursionBase):
    image: Optional[str]


class Excursion(ExcursionBase):
    id: int
    image: Optional[str]
    questions: List[Question] = Field(default=[])

    class Config:
        orm_mode = True


class UserExcursions(ExcursionBase):
    id: int

    class Config:
        orm_mode = True
