import fastapi
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import base, crud, schemas

router = APIRouter(
    prefix="/api/excursions",
    tags=["Excursions"],
    dependencies=[Depends(crud.admins.get_current_admin)],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def create_excursion(
    excursion: schemas.ExcursionCreate,
    session: AsyncSession = Depends(base.get_session),
):
    await crud.excursions.create_excursion(excursion=excursion, db=session)
    return {
        "excursion": excursion,
        "message": f"Excursion {excursion.title} was successfully created",
    }


@router.get("/")
async def get_excursions(session: AsyncSession = Depends(base.get_session)):
    excursions = await crud.excursions.get_excursions(db=session)
    return {"excursions": excursions}


@router.get("/{pk}", response_model=schemas.Excursion)
async def retrieve_excursion(
    pk: int, session: AsyncSession = Depends(base.get_session)
):
    excursion = await crud.excursions.retrieve_excursion(pk, session)
    if excursion is None:
        raise fastapi.HTTPException(status_code=404, detail="Excursion not found")

    return excursion


@router.put("/{pk}", response_model=schemas.Excursion)
async def update_excursion(
    pk: int,
    data: schemas.ExcursionCreate,
    session: AsyncSession = Depends(base.get_session),
):
    excursion = await crud.excursions.retrieve_excursion(pk, session)
    if excursion is None:
        raise fastapi.HTTPException(status_code=404, detail="Excursion not found")
    return await crud.excursions.update_excursion(excursion, data, session)


@router.delete("/{pk}")
async def delete_excursion_endpoint(
    pk: int, session: AsyncSession = Depends(base.get_session)
):
    excursion = await crud.excursions.retrieve_excursion(pk, session)
    if excursion is None:
        raise fastapi.HTTPException(status_code=404, detail="Excursion not found")

    await crud.excursions.delete_excursion(excursion, session)
    return {f"Excursion {pk} successfully deleted"}


@router.post("/questions/{excursion_pk}", response_model=schemas.Question)
async def create_excursion_questions(
    excursion_pk: int,
    question: schemas.QuestionCreate,
    session: AsyncSession = Depends(base.get_session),
):
    db_excursion = await crud.excursions.retrieve_excursion(
        e_id=excursion_pk, db=session
    )
    if db_excursion is None:
        raise fastapi.HTTPException(status_code=404, detail="Excursion not found")
    question = await crud.questions.create_question(
        question=question, db=session, excursion_id=excursion_pk
    )
    return question
