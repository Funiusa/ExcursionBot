from typing import List, Annotated, Dict

import fastapi
from fastapi import Depends, security, APIRouter
from sqlalchemy.orm import Session

from database import models, schemas, services

router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/users", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(services.get_db)):
    return await services.create_user(user=user, db=db)


@router.get("/users", response_model=List[schemas.User])
async def get_users(
    db: Session = Depends(services.get_db),
) -> List[schemas.User]:
    users = await services.get_users(db)
    return users


@router.get("/users/{pk}", response_model=schemas.User)
async def retrieve_user(pk: int, db: Session = Depends(services.get_db)):
    user = await services.retrieve_user(pk, db)
    if user is None:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(services.get_db)):
    user = await services.retrieve_user(user_id, db)
    if user is None:
        raise fastapi.HTTPException(status_code=404, detail="User not found")

    await services.delete_user(user, db)
    return {f"User {user_id} was successfully deleted"}
