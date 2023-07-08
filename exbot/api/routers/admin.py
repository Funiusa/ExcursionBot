from fastapi import APIRouter, Depends, status, Body, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.jwt_handler import auth_handler
from database import schemas
from database import base
from database.crud import admins

router = APIRouter(
    prefix="/api/admins",
    tags=["Admins"],
    dependencies=[Depends(admins.get_current_admin)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_admins(session: "AsyncSession" = Depends(base.get_session)):
    admins_list = await admins.get_admins(session)
    return {"admins": admins_list}


@router.post("/register", dependencies=[Depends(admins.get_current_superuser)])
async def register_create_admin(
    session: AsyncSession = Depends(base.get_session),
    admin_data: schemas.AdminCreate = Body(default=None),
):
    try:
        admin = await admins.get_admin_by_username(admin_data.username, session)
        if admin:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Admin already exists"
            )
        admin_data.password = auth_handler.get_password_hash(
            password=admin_data.password
        )
        admin = await admins.create_admin(admin=admin_data, db=session)
        return {f"Admin with username: '{admin.username}' was successfully created"}
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Email already in use",
        )


@router.get("/{admin_id}")
async def retrieve_admin(
    admin_id: int, session: AsyncSession = Depends(base.get_session)
) -> schemas.Admin:
    admin = await admins.retrieve_admin(admin_id, session)
    return admin


@router.put("/{admin_id}")
async def update_admin(
    admin_id: int,
    data: schemas.AdminCreate,
    session: AsyncSession = Depends(base.get_session),
):
    admin = await admins.retrieve_admin(admin_id=admin_id, db=session)
    updated_admin = await admins.update_admin(admin=admin, data=data, db=session)

    return {"success": f"Admin {admin_id} was updated", "result": updated_admin}


@router.delete("/{admin_id}", dependencies=[Depends(admins.get_current_superuser)])
async def delete_admin(
    admin_id: int, session: AsyncSession = Depends(base.get_session)
):
    admin = await admins.retrieve_admin(admin_id=admin_id, db=session)
    if admin.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Superuser cannot be removed"
        )
    await admins.delete_admin(admin=admin, db=session)
    return {f"Admin with ID {admin_id} was successfully deleted"}
