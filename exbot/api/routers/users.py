from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import base, crud, schemas

router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
    dependencies=[Depends(crud.admins.get_current_admin)],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def create_user(
    user: schemas.UserCreate, session: AsyncSession = Depends(base.get_session)
):
    user = await crud.users.create_user(user=user, db=session)
    return {"user": user, "message": f"User {user.username} was successfully created"}


@router.get("/", response_model=List[schemas.User])
async def get_users(
    session: AsyncSession = Depends(base.get_session),
) -> List[schemas.User]:
    users = await crud.users.get_users(session)
    return users


@router.get("/{pk}", response_model=schemas.User)
async def retrieve_user(pk: int, session: AsyncSession = Depends(base.get_session)):
    user = await crud.users.retrieve_user(pk, session)
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(base.get_session)):
    user = await crud.users.retrieve_user(user_id, session)
    await crud.users.delete_user(user, session)
    return {f"User with ID {user_id} was successfully deleted"}
