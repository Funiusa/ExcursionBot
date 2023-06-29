from typing import List

import fastapi
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database.base import Base, engine, SessionLocal
from database import models, schemas


def create_database():
    with engine.begin() as conn:
        # Base.metadata.drop_all(conn)
        Base.metadata.create_all(conn)


def get_db() -> Session:
    with SessionLocal() as session:
        yield session


async def create_user(user: schemas.UserCreate, db: "Session") -> schemas.User:
    user = models.User(**user.dict())
    db.add(user)
    try:
        db.commit()
        return user
    except IntegrityError as ex:
        db.rollback()
        raise fastapi.HTTPException(status_code=404, detail=f"Exception: {ex}")


async def get_users(db: Session) -> List[models.User]:
    users = db.query(models.User).all()
    return list(map(schemas.User.from_orm, users))


async def get_user_by_user_id(user_id: int, db: "Session"):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    return user


async def retrieve_user(id: int, db: "Session") -> schemas.User:
    result = db.execute(select(models.User).where(models.User.id == id))
    user = result.first()
    return schemas.User.from_orm(user)


async def create_excursion(
        excursion: schemas.ExcursionCreate, db: "Session"
) -> schemas.Excursion:
    excursion = models.Excursion(**excursion.dict())
    db.add(excursion)
    try:
        db.commit()
        return schemas.Excursion.from_orm(excursion)
    except IntegrityError as ex:
        db.rollback()
        raise fastapi.HTTPException(status_code=404, detail=f"Error: {ex}")


async def get_excursions(db: "Session") -> List[schemas.Excursion]:
    result = db.execute(select(models.Excursion))
    excursions = result.scalars().all()
    return list(map(schemas.Excursion.from_orm, excursions))


async def get_excursion_by_title(title: str, db: "Session") -> models.Excursion:
    result = db.execute(select(models.Excursion).where(models.Excursion.title == title))
    excursion = result.scalars().first()
    return excursion


async def retrieve_excursion(e_id: int, db: "Session"):
    try:
        result = db.execute(select(models.Excursion).where(models.Excursion.id == e_id))
        excursion = result.scalars().first()
        return excursion
    except IntegrityError:
        db.rollback()
        raise fastapi.HTTPException(status_code=404, detail="Excursion doesn't exists")


async def update_excursion(
        excursion: models.Excursion, data: schemas.ExcursionCreate, db: "Session"
):
    excursion.title = data.title
    excursion.intro = data.intro
    excursion.description = data.description
    excursion.is_published = data.is_published
    excursion.image = data.image
    db.commit()
    db.refresh(excursion)
    return schemas.Excursion.from_orm(excursion)


async def delete_excursion(excursion: models.Excursion, db: "Session"):
    db.delete(excursion)
    db.commit()


async def create_question(
        question: schemas.QuestionCreate, db: "Session", excursion_id: int
) -> schemas.Question:
    question = models.Question(**question.dict(), excursion_id=excursion_id)
    db.add(question)
    try:
        db.commit()
        db.refresh(question)
        return question
    except IntegrityError as ex:
        db.rollback()
        raise fastapi.HTTPException(status_code=404, detail=f"Error: {ex}")


async def get_questions(db: "Session") -> List[schemas.Question]:
    result = db.execute(select(models.Question))
    questions = result.scalars().all()
    return list(map(schemas.Question.from_orm, questions))


async def retrieve_question(q_id: int, db: "Session"):
    try:
        result = db.execute(select(models.Question).where(models.Question.id == q_id))
        question = result.scalars().first()
        return question
    except IntegrityError:
        db.rollback()
        raise fastapi.HTTPException(status_code=404, detail="Question doesn't exists")


async def update_question(
        question: models.Question, data: schemas.QuestionCreate, db: "Session"
):
    question.place = data.place
    question.answer = data.answer
    question.hint = data.hint
    question.text = data.text
    question.correct = data.correct
    question.addition = data.addition
    question.final = data.final

    db.commit()
    db.refresh(question)
    return schemas.Question.from_orm(question)


async def delete_question(question: models.Question, db: "Session"):
    db.delete(question)
    # db.commit()


async def delete_user(user: models.User, db: "Session"):
    db.delete(user)
    db.commit()
