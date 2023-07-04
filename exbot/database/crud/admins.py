from typing import List

import fastapi
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import models, schemas


async def get_admins(db: "Session") -> List[models.Admin]:
    admins = db.query(models.Admin).all()
    return list(map(schemas.Admin.from_orm, admins))


async def get_admin_by_email(email: str, db: "Session"):
    admin = db.query(models.Admin).where(models.Admin.email == email).first()
    return admin


async def get_admin_by_username(username: str, db: "Session"):
    admin = db.query(models.Admin).filter_by(username=username).first()
    return admin


async def create_admin(admin: schemas.AdminCreate, db: "Session") -> schemas.Admin:
    admin = models.Admin(**admin.dict())
    db.add(admin)
    try:
        db.commit()
        db.refresh(admin)
        return admin
    except IntegrityError as ex:
        db.rollback()
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=f"Exception: {ex}"
        )


async def retrieve_admin(admin_id: int, db: "Session") -> schemas.Admin:
    try:
        result = db.execute(select(models.Admin).filter_by(id=admin_id))
        admin = result.scalars().first()
        if not admin:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"Admin with ID {admin_id} doesn't exists",
            )
        return schemas.Admin.from_orm(admin)
    except IntegrityError:
        db.rollback()
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Admin with ID {admin_id} doesn't exists",
        )


async def delete_admin(admin: models.Admin, db: "Session"):
    db.delete(admin)
    db.commit()
