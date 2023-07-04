from sqlalchemy.ext.asyncio import AsyncSession
from database.base import Base, async_engine, SessionAsync


async def create_async_database():
    async with async_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with SessionAsync() as session:
        yield session
