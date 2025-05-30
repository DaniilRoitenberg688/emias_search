from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from config import config
from sqlalchemy.ext.asyncio import AsyncSession

DATABASE_URL = config.DATABASE_URL

engine = create_async_engine(DATABASE_URL)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session