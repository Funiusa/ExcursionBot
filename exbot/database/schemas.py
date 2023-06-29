from typing import List, Optional

from pydantic import BaseModel


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


class ExcursionBase(BaseModel):
    title: str
    intro: str
    description: str
    image: str
    is_published: bool = False


class ExcursionCreate(ExcursionBase):
    pass


class Excursion(ExcursionBase):
    id: int
    questions: List[Question] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    user_id: int
    username: str
    phone: str


class UserCreate(UserBase):
    excursions: List[ExcursionCreate] = []


class User(UserBase):
    id: int
    excursions: List[Excursion] = []

    class Config:
        orm_mode = True


class UserListResponse(BaseModel):
    users: List[User]
