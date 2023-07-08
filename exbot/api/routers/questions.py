from typing import List

import fastapi
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import base, crud, schemas

router = APIRouter(
    prefix="/api/questions",
    tags=["Questions"],
    dependencies=[Depends(crud.admins.get_current_admin)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[schemas.Question])
async def get_questions(
    session: AsyncSession = Depends(base.get_session),
) -> List[schemas.Question]:
    return await crud.questions.get_questions(db=session)


@router.get("/{pk}", response_model=schemas.Question)
async def retrieve_question(pk: int, session: AsyncSession = Depends(base.get_session)):
    question = await crud.questions.retrieve_question(pk, session)
    if question is None:
        raise fastapi.HTTPException(status_code=404, detail="Question not found")

    return question


@router.put("/{pk}", response_model=schemas.Question)
async def update_question(
    pk: int,
    data: schemas.QuestionCreate,
    session: AsyncSession = Depends(base.get_session),
):
    question = await crud.questions.retrieve_question(pk, session)
    if question is None:
        raise fastapi.HTTPException(status_code=404, detail="Question not found")
    return await crud.questions.update_question(question, data, session)


@router.delete("/{question_id}")
async def delete_question(
    question_id: int, session: AsyncSession = Depends(base.get_session)
):
    question = await crud.questions.retrieve_question(question_id, session)
    if question is None:
        raise fastapi.HTTPException(status_code=404, detail="Question not found")
    await crud.questions.delete_question(question, session)
    return {"Question was successfully deleted"}
