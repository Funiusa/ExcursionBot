from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncAttrs,
)

from sqlalchemy.orm import DeclarativeBase
from config import url


async_engine = create_async_engine(url, echo=True)
SessionAsync = async_sessionmaker(
    autoflush=False, bind=async_engine, class_=AsyncSession, expire_on_commit=False
)
async_session = SessionAsync()


class Base(AsyncAttrs, DeclarativeBase):
    pass
