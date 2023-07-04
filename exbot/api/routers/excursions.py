from typing import Annotated

import fastapi
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth import jwt_handler
from database import schemas, services, crud
from api.auth.jwt_handler import get_current_admin

router = APIRouter(
    prefix="/api/excursions",
    tags=["Excursions"],
    # dependencies=[Depends(get_current_admin)],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def create_excursion(
    excursion: schemas.ExcursionCreate, db: AsyncSession = Depends(services.get_session)
):
    await crud.excursions.create_excursion(excursion=excursion, db=db)
    return {
        "excursion": excursion,
        "message": f"Excursion {excursion.title} was successfully created",
    }


@router.get("/")
async def get_excursions(
    # token: Annotated[str, Depends(jwt_handler.oauth2schema)],
    db: AsyncSession = Depends(services.get_session),
):
    excursions = await crud.excursions.get_excursions(db=db)
    return {"excursions": excursions}


@router.get("/{pk}", response_model=schemas.Excursion)
async def retrieve_excursion(pk: int, db: AsyncSession = Depends(services.get_session)):
    excursion = await crud.excursions.retrieve_excursion(pk, db)
    if excursion is None:
        raise fastapi.HTTPException(status_code=404, detail="Excursion not found")

    return excursion


@router.put("/{pk}", response_model=schemas.Excursion)
async def update_excursion(
    pk: int,
    data: schemas.ExcursionCreate,
    db: AsyncSession = Depends(services.get_session),
):
    excursion = await crud.excursions.retrieve_excursion(pk, db)
    if excursion is None:
        raise fastapi.HTTPException(status_code=404, detail="Excursion not found")
    return await crud.excursions.update_excursion(excursion, data, db)


@router.delete("/{pk}")
async def delete_excursion_endpoint(
    pk: int, db: AsyncSession = Depends(services.get_session)
):
    excursion = await crud.excursions.retrieve_excursion(pk, db)
    if excursion is None:
        raise fastapi.HTTPException(status_code=404, detail="Excursion not found")

    await crud.excursions.delete_excursion(excursion, db)
    return {f"Excursion {pk} successfully deleted"}


@router.post("/questions/{excursion_pk}", response_model=schemas.Question)
async def create_excursion_questions(
    excursion_pk: int,
    question: schemas.QuestionCreate,
    db: AsyncSession = Depends(services.get_session),
):
    db_excursion = await crud.excursions.retrieve_excursion(e_id=excursion_pk, db=db)
    if db_excursion is None:
        raise fastapi.HTTPException(status_code=404, detail="Excursion not found")
    question = await crud.questions.create_question(
        question=question, db=db, excursion_id=excursion_pk
    )
    return question
