from typing import List

import fastapi
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from database import models, schemas, base
from api.auth.jwt_handler import auth_handler


async def create_admin(admin: schemas.AdminCreate, db: "AsyncSession") -> schemas.Admin:
    admin = models.Admin(**admin.dict())
    db.add(admin)
    try:
        await db.commit()
        return admin
    except IntegrityError:
        await db.rollback()
        raise fastapi.HTTPException(status_code=404, detail="Admin was not created")


async def get_admins(db: "AsyncSession") -> List[models.Admin]:
    stmt = select(models.Admin)
    result = await db.execute(statement=stmt)
    return list(map(schemas.Admin.from_orm, result.scalars()))


async def get_admin_by_email(email: str, db: "AsyncSession") -> models.Admin:
    try:
        stmt = select(models.Admin).filter_by(email=email)
        result = await db.execute(statement=stmt)
        admin = result.scalars().first()
        return admin
    except Exception:
        raise fastapi.HTTPException(status_code=500, detail=f"{email} doesn't exist")


async def get_admin_by_username(username: str, db: "AsyncSession") -> models.Admin:
    try:
        stmt = select(models.Admin).filter_by(username=username)
        result = await db.execute(statement=stmt)
        admin = result.scalars().first()
        return admin
    except Exception:
        raise fastapi.HTTPException(status_code=500, detail=f"{username}")


async def get_current_admin(
    db: "AsyncSession" = fastapi.Depends(base.get_session),
    token: str = fastapi.Depends(auth_handler.get_login_token()),
):
    try:
        payload = auth_handler.decode_token(token)
        email = payload.get("email")
        admin = await get_admin_by_email(email=email, db=db)
    except fastapi.HTTPException:
        raise fastapi.HTTPException(status_code=401, detail="Invalid credentials")
    return schemas.Admin.from_orm(admin)


async def get_current_superuser(
    db: "AsyncSession" = fastapi.Depends(base.get_session),
    token: str = fastapi.Depends(auth_handler.get_login_token()),
):
    try:
        payload = auth_handler.decode_token(token)
        email = payload.get("email")
        admin = await get_admin_by_email(email=email, db=db)
    except fastapi.HTTPException:
        raise fastapi.HTTPException(status_code=401, detail="Invalid credentials")
    if not admin.is_superuser:
        raise fastapi.HTTPException(status_code=401, detail="Only superuser")

    return schemas.Admin.from_orm(admin)


async def retrieve_admin(admin_id: int, db: "AsyncSession") -> schemas.Admin:
    try:
        stmt = select(models.Admin).filter_by(id=admin_id)
        result = await db.execute(statement=stmt)
        admin = result.scalars().first()
        if not admin:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"Admin with ID {admin_id} doesn't exists",
            )
        return admin
    except IntegrityError:
        await db.rollback()
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Admin with ID {admin_id} doesn't exists",
        )


async def delete_admin(admin: models.Admin, db: "AsyncSession"):
    await db.delete(admin)
    await db.commit()
