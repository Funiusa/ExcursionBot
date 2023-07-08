from typing import List

import fastapi
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import models, schemas


async def create_user(user: schemas.UserCreate, db: "AsyncSession") -> schemas.User:
    user = models.User(**user.dict())
    db.add(user)
    try:
        await db.commit()
        return user
    except IntegrityError:
        await db.rollback()
        raise fastapi.HTTPException(
            status_code=404, detail=f"username or phone number already in use"
        )
    except SQLAlchemyError as ex:
        await db.rollback()
        raise fastapi.HTTPException(status_code=500, detail=f"Exception: {ex}")


async def get_users(
    db: "AsyncSession", skip: int = 0, limit: int = 100
) -> List[models.User]:
    stmt = (
        select(models.User)
        .options(
            selectinload(models.User.excursions).options(
                selectinload(models.Excursion.questions)
            )
        )
        .limit(limit=limit)
        .offset(skip)
    )
    result = await db.execute(statement=stmt)
    return list(map(schemas.User.from_orm, result.scalars()))


async def get_user_by_telegram_id(telegram_id: int, db: "AsyncSession"):
    try:
        stmt = select(models.User).options(selectinload(models.User.excursions))
        result = await db.execute(stmt.filter_by(telegram_id=telegram_id))
        user = result.scalars().first()
        return user
    except IntegrityError:
        await db.rollback()
        raise fastapi.HTTPException(status_code=404, detail="User doesn't exists")


async def retrieve_user(user_id: int, db: "AsyncSession") -> schemas.User:
    try:
        stmt = select(models.User).options(selectinload(models.User.excursions))
        result = await db.execute(stmt.filter_by(id=user_id))
        user = result.scalars().first()
        if not user:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"Admin with ID {user_id} doesn't exists",
            )
        return user
    except IntegrityError:
        await db.rollback()
        raise fastapi.HTTPException(status_code=404, detail="User doesn't exists")


async def delete_user(user: models.User, db: "AsyncSession"):
    await db.delete(user)
    await db.commit()
