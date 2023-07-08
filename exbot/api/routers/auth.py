from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.jwt_handler import auth_handler
from database.base import get_session
from database.crud import admins

router = APIRouter(
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/login/token")
async def login_admin(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    admin = await admins.get_admin_by_username(form_data.username, session)
    if not admin or not auth_handler.verify_password(
        form_data.password, admin.password
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Authentication error"
        )
    data = {"id": admin.id, "username": admin.username, "email": admin.email}
    token = auth_handler.encode_token(data=data)

    return {"token_type": "Bearer", "access_token": token}
