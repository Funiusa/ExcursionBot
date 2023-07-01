from datetime import timedelta
from typing import List, Annotated, Dict

import fastapi
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from database import models, schemas, services
from database.services import create_access_token

router = APIRouter(
    prefix="/admin",
    tags=["Auth"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/login",
)
async def admin_login(
    admin_data: schemas.AdminLogin, db: "Session" = Depends(services.get_db)
):
    admin = db.query(models.Admin).filter_by(username=admin_data.username).first()
    if not admin or not admin.verify_password(admin_data.password):
        raise fastapi.HTTPException(
            status_code=401, detail="Invalid username or password"
        )
    token = create_access_token(
        data={"sub": admin.username}, expires_delta=timedelta(30)
    )
    return {"access_token": token, "token_type": "bearer"}


@router.get("/admins")
async def get_admins(db: Session = Depends(services.get_db)):
    admins = await services.get_admins(db)
    return {"admins": admins}


@router.get("/users", response_model=schemas.Admin)
async def get_current_admin(admin: schemas.Admin = Depends(services.get_current_admin)):
    return admin
