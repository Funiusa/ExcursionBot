from typing import List

import fastapi
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import models, schemas, services

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello! Happy birthday! Good luck to you)"}


@app.post("/api/users", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(services.get_db)):
    return await services.create_user(user=user, db=db)


@app.get("/api/users", response_model=List[schemas.User])
async def get_users(db: Session = Depends(services.get_db)) -> List[schemas.User]:
    users = await services.get_users(db)
    return users


@app.get("/api/users/{pk}", response_model=schemas.User)
async def retrieve_user(pk: int, db: Session = Depends(services.get_db)):
    return await services.retrieve_user(pk, db)


@app.post("/api/excursions", response_model=schemas.Excursion)
async def create_excursion(
        excursion: schemas.ExcursionCreate, db: Session = Depends(services.get_db)
):
    return await services.create_excursion(excursion=excursion, db=db)


@app.get("/api/excursions", response_model=List[schemas.Excursion])
async def get_excursions(
        db: Session = Depends(services.get_db),
) -> List[schemas.Excursion]:
    return await services.get_excursions(db=db)


@app.get("/api/excursions/{pk}", response_model=schemas.Excursion)
async def retrieve_excursion(pk: int, db: Session = Depends(services.get_db)):
    excursion = await services.retrieve_excursion(pk, db)
    if excursion is None:
        raise fastapi.HTTPException(status_code=404, detail="Excursion not found")

    return excursion


@app.put("/api/excursions/{pk}", response_model=schemas.Excursion)
async def update_excursion(
        pk: int, data: schemas.ExcursionCreate, db: Session = Depends(services.get_db)
):
    excursion = await services.retrieve_excursion(pk, db)
    if excursion is None:
        raise fastapi.HTTPException(status_code=404, detail="Excursion not found")
    return await services.update_excursion(excursion, data, db)


@app.delete("/api/excursions/{pk}", response_model=schemas.Excursion)
async def delete_excursion_endpoint(pk: int, db: Session = Depends(services.get_db)):
    excursion = await services.retrieve_excursion(pk, db)
    if excursion is None:
        raise fastapi.HTTPException(status_code=404, detail="Excursion not found")

    await services.delete_excursion(excursion, db)
    return {"message": f"Excursion {pk} successfully deleted"}


@app.post("/api/excursions/{excursion_pk}/questions/", response_model=schemas.Question)
async def create_excursion_questions(
        excursion_pk: int,
        question: schemas.QuestionCreate,
        db: Session = Depends(services.get_db)
):
    db_excursion = await services.retrieve_excursion(e_id=excursion_pk, db=db)
    if db_excursion is None:
        raise fastapi.HTTPException(status_code=404, detail="Excursion not found")
    question = await services.create_question(
        question=question, db=db, excursion_id=excursion_pk
    )
    return question


@app.get("/api/questions", response_model=List[schemas.Question])
async def get_questions(
        db: Session = Depends(services.get_db),
) -> List[schemas.Question]:
    return await services.get_questions(db=db)


@app.get("/api/questions/{pk}", response_model=schemas.Question)
async def retrieve_question(pk: int, db: Session = Depends(services.get_db)):
    question = await services.retrieve_question(pk, db)
    if question is None:
        raise fastapi.HTTPException(status_code=404, detail="Question not found")

    return question


@app.put("/api/questions/{pk}", response_model=schemas.Question)
async def update_question(
        pk: int, data: schemas.QuestionCreate, db: Session = Depends(services.get_db)
):
    question = await services.retrieve_question(pk, db)
    if question is None:
        raise fastapi.HTTPException(status_code=404, detail="Question not found")
    return await services.update_question(question, data, db)


@app.delete("/api/questions/{question_id}", response_model=schemas.Question)
async def delete_question(question_id: int, db: Session = Depends(services.get_db)):
    # question = await services.retrieve_question(question_id, db)
    question = db.get(models.Question, question_id)
    if question is None:
        raise fastapi.HTTPException(status_code=404, detail="Question not found")
    db.delete(question)
    db.commit()

    # await services.delete_question(question, db)
    return


@app.delete("/api/users/{user_id}", response_model=schemas.User)
async def delete_user(user_id: int, db: Session = Depends(services.get_db)):
    user = await services.retrieve_user(user_id, db)
    if user is None:
        raise fastapi.HTTPException(status_code=404, detail="User not found")

    await services.delete_user(user, db)
    return f"Question {user_id} successfully deleted"
