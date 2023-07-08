import fastapi
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.orm import DeclarativeBase

import config
import database
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncAttrs,
)

from api.auth.jwt_handler import auth_handler


class Base(AsyncAttrs, DeclarativeBase):
    pass


async_engine = create_async_engine(config.url, echo=True)
AsyncSessionLocal = async_sessionmaker(
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

db = AsyncSessionLocal()


async def create_all():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


async def get_admin_db(session: AsyncSession = fastapi.Depends(get_session)):
    yield SQLAlchemyUserDatabase(session=session, user_table=database.models.Admin)


async def create_superuser():
    superuser = database.models.Admin(
        telegram_id=config.SU_USER_TELEGRAM,
        username=config.SU_USERNAME,
        email=config.SU_USER_EMAIL,
        password=auth_handler.get_password_hash(config.SU_USER_PASS),
        is_superuser=True,
    )
    async with AsyncSessionLocal() as session:
        session.add(instance=superuser)
        await session.commit()
