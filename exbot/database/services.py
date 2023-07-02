from datetime import timedelta, datetime
from typing import List

import fastapi
import jwt
import sqlalchemy
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from database.base import Base, engine, SessionLocal
from database import models, schemas
import fastapi.security as _security

from passlib import hash

JWT_SECRET = "myjwtsecret"
oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME = timedelta(minutes=30)


def create_database():
    with engine.begin() as conn:
        Base.metadata.drop_all(conn)
        Base.metadata.create_all(conn)


def get_db() -> Session:
    with SessionLocal() as session:
        yield session


async def get_admins(db: "Session") -> List[models.Admin]:
    admins = db.query(models.Admin).all()
    return list(map(schemas.Admin.from_orm, admins))


async def get_admin_by_email(email: str, db: "Session"):
    admin = db.query(models.Admin).where(models.Admin.email == email).first()
    return admin


async def create_admin(admin: schemas.AdminCreate, db: "Session") -> schemas.Admin:

    admin = models.Admin(**admin.dict())
    db.add(admin)
    try:
        db.commit()
        db.refresh(admin)
        return admin
    except IntegrityError as ex:
        db.rollback()
        raise fastapi.HTTPException(status_code=404, detail=f"Exception: {ex}")


async def create_token(admin: models.Admin):
    admin_obj = schemas.Admin.from_orm(admin)
    token = jwt.encode(admin_obj.dict(), JWT_SECRET)
    return dict(access_token=token, token_type="bearer")


# async def authenticate_admin(email: str, password: str, db: "Session"):
#     admin = await get_admin_by_email(email=email, db=db)
#     if not admin:
#         return False
#     if not admin.verify_password(password):
#         return False
#     return admin


async def authenticate_admin(
    token: str = fastapi.Depends(create_token), db: "Session" = fastapi.Depends(get_db)
):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise fastapi.HTTPException(status_code=401, detail="Invalid token")
        # Validate if the user exists and has admin privileges
        admin = db.query(models.Admin).filter_by(username=username).first()
        if not admin:
            raise fastapi.HTTPException(status_code=401, detail="Admin not found")
        # Add additional checks if needed, e.g., check if the user has admin role
        return admin
    except jwt.exceptions.PyJWTError:
        raise fastapi.HTTPException(status_code=401, detail="Invalid token")


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def get_current_admin(
    db: "Session" = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),
):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        admin = db.query(models.Admin).get(payload["id"])
    except:
        raise fastapi.HTTPException(status_code=401, detail="Invalid email or password")
    return schemas.Admin.from_orm(admin)


async def create_user(user: schemas.UserCreate, db: "Session") -> schemas.User:
    user = models.User(**user.dict())
    db.add(user)
    try:
        db.commit()
        return user
    except IntegrityError as ex:
        db.rollback()
        raise fastapi.HTTPException(status_code=404, detail=f"Exception: {ex}")
    except SQLAlchemyError as ex:
        db.rollback()
        raise fastapi.HTTPException(status_code=500, detail=f"Exception: {ex}")


async def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    users = db.query(models.User).offset(skip).limit(limit).all()
    return list(map(schemas.User.from_orm, users))


async def get_user_by_telegram_id(telegram_id: int, db: "Session"):
    try:
        user = db.query(models.User).filter_by(telegram_id=telegram_id).first()
        return user
    except IntegrityError:
        db.rollback()
        raise fastapi.HTTPException(status_code=404, detail="User doesn't exists")


async def retrieve_user(user_id: int, db: "Session") -> schemas.User:
    try:
        result = db.execute(select(models.User).where(models.User.id == user_id))
        user = result.scalars().first()
        return user
    except IntegrityError:
        db.rollback()
        raise fastapi.HTTPException(status_code=404, detail="User doesn't exists")


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
    db.commit()


async def delete_user(user: models.User, db: "Session"):
    db.delete(user)
    db.commit()
