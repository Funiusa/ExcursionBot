from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from typing import Union

from sqlalchemy.orm import sessionmaker


def create_engine(url: Union[URL, str]) -> AsyncEngine:
    return create_async_engine(url=url, echo=True, pool_pre_ping=True)


async def proceed_schemas(engine: AsyncEngine, metadata) -> None:
    async with engine.connect() as connect:
        await connect.run_sync(metadata.create_all)


def get_session_maker(session: AsyncSession) -> sessionmaker:
    return sessionmaker()
