from typing import List

import fastapi
from fastapi import Depends, security, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from database import schemas, services, crud

router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def create_user(
    user: schemas.UserCreate, db: AsyncSession = Depends(services.get_session)
):
    user = await crud.users.create_user(user=user, db=db)
    return {"user": user, "message": f"User {user.username} was successfully created"}


@router.get("/", response_model=List[schemas.User])
async def get_users(
    db: AsyncSession = Depends(services.get_session),
) -> List[schemas.User]:
    users = await crud.users.get_users(db)
    return users


@router.get("/", response_model=schemas.UserListResponse)
async def get_users_ex(
    db: AsyncSession = Depends(services.get_session),
) -> List[schemas.User]:
    users = await crud.users.get_users(db)
    return users


@router.get("/{pk}", response_model=schemas.User)
async def retrieve_user(pk: int, db: AsyncSession = Depends(services.get_session)):
    user = await crud.users.retrieve_user(pk, db)
    if user is None:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(services.get_session)):
    user = await crud.users.retrieve_user(user_id, db)
    if user is None:
        raise fastapi.HTTPException(status_code=404, detail="Excursion not found")

    await crud.users.delete_user(user, db)
    return {f"User {user_id} was successfully deleted"}
