from typing import List, Annotated, Dict

import fastapi
from fastapi import FastAPI, Depends, security
from sqlalchemy.orm import Session

from database import models, schemas, services

app = FastAPI()


# services.create_database()


@app.get("/", tags=["Index"])
async def root():
    return {"message": "Hello! Happy birthday! Good luck to you)"}


@app.post("/api/token/", tags=["Auth"])
async def generate_token(
        form_data: security.OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(services.get_db)
):
    admin = await services.authenticate_admin(
        email=form_data.username, password=form_data.password, db=db
    )
    if not admin:
        raise fastapi.HTTPException(status_code=401, detail="Not valid credential")
    return await services.create_token(admin)


@app.post("/api/admins", tags=["Admins"])
async def create_admin(
        admin: schemas.AdminCreate, db: Session = Depends(services.get_db)
):
    db_admin = await services.get_admin_by_email(email=admin.email, db=db)
    if db_admin:
        raise fastapi.HTTPException(status_code=400, detail="Email already in use")
    await services.create_admin(admin=admin, db=db)
    return await services.create_token(admin)


@app.get("/api/admins", tags=["Admins"])
async def get_admins(db: Session = Depends(services.get_db)):
    admins = await services.get_admins(db)
    return {"admins": admins}


@app.get("api/users", response_model=schemas.Admin, tags=["Users"])
async def get_current_admin(admin: schemas.Admin = Depends(services.get_current_admin)):
    return admin


@app.post("/api/users", response_model=schemas.User, tags=["Users"])
async def create_user(user: schemas.UserCreate, db: Session = Depends(services.get_db)):
    return await services.create_user(user=user, db=db)


@app.get("/api/users", response_model=List[schemas.User], tags=["Users"])
async def get_users(
        db: Session = Depends(services.get_db),
) -> List[schemas.User]:
    users = await services.get_users(db)
    return users


@app.get("/api/users/{pk}", response_model=schemas.User, tags=["Users"])
async def retrieve_user(pk: int, db: Session = Depends(services.get_db)):
    user = await services.retrieve_user(pk, db)
    if user is None:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/api/users/{user_id}", tags=["Users"])
async def delete_user(user_id: int, db: Session = Depends(services.get_db)):
    user = await services.retrieve_user(user_id, db)
    if user is None:
        raise fastapi.HTTPException(status_code=404, detail="User not found")

    await services.delete_user(user, db)
    return {f"User {user_id} was successfully deleted"}


@app.post("/api/excursions", response_model=schemas.Excursion, tags=["Excursions"])
async def create_excursion(
        excursion: schemas.ExcursionCreate, db: Session = Depends(services.get_db)
):
    return await services.create_excursion(excursion=excursion, db=db)


@app.get("/api/excursions", tags=["Excursions"])
async def get_excursions(
        token: Annotated[str, Depends(services.oauth2schema)],
        db: Session = Depends(services.get_db),
):
    excursions = await services.get_excursions(db=db)
    return {"excursions": excursions, "token": token}


@app.get("/api/excursions/{pk}", response_model=schemas.Excursion, tags=["Excursions"])
async def retrieve_excursion(pk: int, db: Session = Depends(services.get_db)):
    excursion = await services.retrieve_excursion(pk, db)
    if excursion is None:
        raise fastapi.HTTPException(status_code=404, detail="Excursion not found")

    return excursion


@app.put("/api/excursions/{pk}", response_model=schemas.Excursion, tags=["Excursions"])
async def update_excursion(
        pk: int, data: schemas.ExcursionCreate, db: Session = Depends(services.get_db)
):
    excursion = await services.retrieve_excursion(pk, db)
    if excursion is None:
        raise fastapi.HTTPException(status_code=404, detail="Excursion not found")
    return await services.update_excursion(excursion, data, db)


@app.delete("/api/excursions/{pk}", tags=["Excursions"])
async def delete_excursion_endpoint(pk: int, db: Session = Depends(services.get_db)):
    excursion = await services.retrieve_excursion(pk, db)
    if excursion is None:
        raise fastapi.HTTPException(status_code=404, detail="Excursion not found")

    await services.delete_excursion(excursion, db)
    return {f"Excursion {pk} successfully deleted"}


@app.post(
    "/api/excursions/{excursion_pk}/questions/",
    response_model=schemas.Question,
    tags=["Questions"]
)
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


@app.get("/api/questions", response_model=List[schemas.Question], tags=["Questions"])
async def get_questions(
        db: Session = Depends(services.get_db),
) -> List[schemas.Question]:
    return await services.get_questions(db=db)


@app.get("/api/questions/{pk}", response_model=schemas.Question, tags=["Questions"])
async def retrieve_question(pk: int, db: Session = Depends(services.get_db)):
    question = await services.retrieve_question(pk, db)
    if question is None:
        raise fastapi.HTTPException(status_code=404, detail="Question not found")

    return question


@app.put("/api/questions/{pk}", response_model=schemas.Question, tags=["Questions"])
async def update_question(
        pk: int, data: schemas.QuestionCreate, db: Session = Depends(services.get_db)
):
    question = await services.retrieve_question(pk, db)
    if question is None:
        raise fastapi.HTTPException(status_code=404, detail="Question not found")
    return await services.update_question(question, data, db)


@app.delete(
    "/api/questions/{question_id}", tags=["Questions"]
)
async def delete_question(question_id: int, db: Session = Depends(services.get_db)):
    question = await services.retrieve_question(question_id, db)
    if question is None:
        raise fastapi.HTTPException(status_code=404, detail="Question not found")
    await services.delete_question(question, db)
    return {"Question was successfully deleted"}
