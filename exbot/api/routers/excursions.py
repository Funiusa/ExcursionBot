from typing import List, Annotated, Dict

import fastapi
from fastapi import Depends, security, APIRouter
from sqlalchemy.orm import Session

from database import models, schemas, services

router = APIRouter(
    prefix="/api/excursions",
    tags=["Excursions"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/excursions", response_model=schemas.Excursion)
async def create_excursion(
    excursion: schemas.ExcursionCreate, db: Session = Depends(services.get_db)
):
    return await services.create_excursion(excursion=excursion, db=db)


@router.get("/excursions")
async def get_excursions(
    token: Annotated[str, Depends(services.oauth2schema)],
    db: Session = Depends(services.get_db),
):
    excursions = await services.get_excursions(db=db)
    return {"excursions": excursions, "token": token}


@router.get("/excursions/{pk}", response_model=schemas.Excursion)
async def retrieve_excursion(pk: int, db: Session = Depends(services.get_db)):
    excursion = await services.retrieve_excursion(pk, db)
    if excursion is None:
        raise fastapi.HTTPException(status_code=404, detail="Excursion not found")

    return excursion


@router.put("/excursions/{pk}", response_model=schemas.Excursion)
async def update_excursion(
    pk: int, data: schemas.ExcursionCreate, db: Session = Depends(services.get_db)
):
    excursion = await services.retrieve_excursion(pk, db)
    if excursion is None:
        raise fastapi.HTTPException(status_code=404, detail="Excursion not found")
    return await services.update_excursion(excursion, data, db)


@router.delete("/excursions/{pk}")
async def delete_excursion_endpoint(pk: int, db: Session = Depends(services.get_db)):
    excursion = await services.retrieve_excursion(pk, db)
    if excursion is None:
        raise fastapi.HTTPException(status_code=404, detail="Excursion not found")

    await services.delete_excursion(excursion, db)
    return {f"Excursion {pk} successfully deleted"}


@router.post("/excursions/{excursion_pk}/questions/", response_model=schemas.Question)
async def create_excursion_questions(
    excursion_pk: int,
    question: schemas.QuestionCreate,
    db: Session = Depends(services.get_db),
):
    db_excursion = await services.retrieve_excursion(e_id=excursion_pk, db=db)
    if db_excursion is None:
        raise fastapi.HTTPException(status_code=404, detail="Excursion not found")
    question = await services.create_question(
        question=question, db=db, excursion_id=excursion_pk
    )
    return question
