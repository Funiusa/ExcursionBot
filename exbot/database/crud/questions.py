from typing import List

import fastapi
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database import models, schemas


async def create_question(
    question: schemas.QuestionCreate, db: "AsyncSession", excursion_id: int
) -> schemas.Question:
    question = models.Question(**question.dict(), excursion_id=excursion_id)
    db.add(question)
    try:
        await db.commit()
        await db.refresh(question)
        return question
    except IntegrityError as ex:
        await db.rollback()
        raise fastapi.HTTPException(status_code=404, detail=f"Error: {ex}")


async def get_questions(db: "AsyncSession") -> List[schemas.Question]:
    result = await db.execute(select(models.Question))
    questions = result.scalars().all()
    return list(map(schemas.Question.from_orm, questions))


async def retrieve_question(q_id: int, db: "AsyncSession"):
    try:
        result = await db.execute(select(models.Question).filter_by(id=q_id))
        question = result.scalars().first()
        return question
    except IntegrityError:
        await db.rollback()
        raise fastapi.HTTPException(status_code=404, detail="Question doesn't exists")


async def update_question(
    question: models.Question, data: schemas.QuestionCreate, db: "AsyncSession"
):
    question.place = data.place
    question.answer = data.answer
    question.hint = data.hint
    question.text = data.text
    question.correct = data.correct
    question.addition = data.addition
    question.final = data.final

    await db.commit()
    await db.refresh(question)
    return schemas.Question.from_orm(question)


async def delete_question(question: models.Question, db: "AsyncSession"):
    await db.delete(question)
    await db.commit()
