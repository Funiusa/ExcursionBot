from typing import List, Annotated, Dict
import fastapi
from fastapi import FastAPI, Depends, security, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from database import schemas, services, crud

router = APIRouter(
    prefix="/api/questions",
    tags=["Questions"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[schemas.Question])
async def get_questions(
    db: AsyncSession = Depends(services.get_session),
) -> List[schemas.Question]:
    return await crud.questions.get_questions(db=db)


@router.get("/{pk}", response_model=schemas.Question)
async def retrieve_question(pk: int, db: AsyncSession = Depends(services.get_session)):
    question = await crud.questions.retrieve_question(pk, db)
    if question is None:
        raise fastapi.HTTPException(status_code=404, detail="Question not found")

    return question


@router.put("/{pk}", response_model=schemas.Question)
async def update_question(
    pk: int,
    data: schemas.QuestionCreate,
    db: AsyncSession = Depends(services.get_session),
):
    question = await crud.questions.retrieve_question(pk, db)
    if question is None:
        raise fastapi.HTTPException(status_code=404, detail="Question not found")
    return await crud.questions.update_question(question, data, db)


@router.delete("/{question_id}")
async def delete_question(
    question_id: int, db: AsyncSession = Depends(services.get_session)
):
    question = await crud.questions.retrieve_question(question_id, db)
    if question is None:
        raise fastapi.HTTPException(status_code=404, detail="Question not found")
    await crud.questions.delete_question(question, db)
    return {"Question was successfully deleted"}
