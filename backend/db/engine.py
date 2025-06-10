from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from config import config
from sqlalchemy.ext.asyncio import AsyncSession

DATABASE_URL = config.DATABASE_URL
DATABASE_URL_PDF = config.DATABASE_URL_PDF

engine = create_async_engine(DATABASE_URL)
engine_pdf = create_async_engine(DATABASE_URL_PDF)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
async_session_maker_pdf = async_sessionmaker(engine_pdf, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


async def get_session_pdf() -> AsyncSession:
    async with async_session_maker_pdf() as session:
        yield session
