from typing import List, Annotated, Dict
import fastapi
from fastapi import FastAPI, Depends, security, APIRouter
from sqlalchemy.orm import Session
from database import models, schemas, services

router = APIRouter(
    prefix="/api/questions",
    tags=["Questions"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/questions", response_model=List[schemas.Question])
async def get_questions(
    db: Session = Depends(services.get_db),
) -> List[schemas.Question]:
    return await services.get_questions(db=db)


@router.get("/questions/{pk}", response_model=schemas.Question)
async def retrieve_question(pk: int, db: Session = Depends(services.get_db)):
    question = await services.retrieve_question(pk, db)
    if question is None:
        raise fastapi.HTTPException(status_code=404, detail="Question not found")

    return question


@router.put("/questions/{pk}", response_model=schemas.Question)
async def update_question(
    pk: int, data: schemas.QuestionCreate, db: Session = Depends(services.get_db)
):
    question = await services.retrieve_question(pk, db)
    if question is None:
        raise fastapi.HTTPException(status_code=404, detail="Question not found")
    return await services.update_question(question, data, db)


@router.delete("/questions/{question_id}")
async def delete_question(question_id: int, db: Session = Depends(services.get_db)):
    question = await services.retrieve_question(question_id, db)
    if question is None:
        raise fastapi.HTTPException(status_code=404, detail="Question not found")
    await services.delete_question(question, db)
    return {"Question was successfully deleted"}
