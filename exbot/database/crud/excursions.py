from typing import List

import fastapi
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import models, schemas


async def create_excursion(
    excursion: schemas.ExcursionCreate, db: "AsyncSession"
) -> schemas.Excursion:
    excursion = models.Excursion(**excursion.dict())
    db.add(excursion)
    try:
        await db.commit()
        return excursion
    except IntegrityError as ex:
        await db.rollback()
        raise fastapi.HTTPException(status_code=404, detail=f"Error: {ex}")


async def get_excursions(db: "AsyncSession") -> List[schemas.Excursion]:
    try:
        stmt = select(models.Excursion).options(
            selectinload(models.Excursion.questions)
        )
        result = await db.execute(statement=stmt)
        excursions = result.scalars().all()
        return list(map(schemas.Excursion.from_orm, excursions))
    except SQLAlchemyError as ex:
        await db.rollback()
        raise fastapi.HTTPException(status_code=500, detail=f"Error: {ex}")


async def get_excursion_by_title(title: str, db: "AsyncSession") -> models.Excursion:
    stmt = select(models.Excursion).options(selectinload(models.Excursion.questions))
    result = await db.execute(statement=stmt.filter_by(title=title))
    excursion = result.scalars().first()
    return excursion


async def retrieve_excursion(e_id: int, db: "AsyncSession"):
    try:
        stmt = select(models.Excursion).options(
            selectinload(models.Excursion.questions)
        )
        result = await db.execute(statement=stmt.filter_by(id=e_id))
        excursion = result.scalars().first()
        return excursion
    except IntegrityError:
        await db.rollback()
        raise fastapi.HTTPException(status_code=404, detail="Excursion doesn't exists")


async def update_excursion(
    excursion: models.Excursion, data: schemas.ExcursionCreate, db: "AsyncSession"
):
    excursion.title = data.title
    excursion.intro = data.intro
    excursion.description = data.description
    excursion.is_published = data.is_published
    excursion.image = data.image
    await db.commit()
    await db.refresh(excursion)
    return schemas.Excursion.from_orm(excursion)


async def delete_excursion(excursion: models.Excursion, db: "AsyncSession"):
    await db.delete(excursion)
    await db.commit()
