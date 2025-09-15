from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from config import config
from sqlalchemy.ext.asyncio import AsyncSession

# Прописываем название приложения. Требуется для корректного анализа запросов в БД при необходимости.
connect_args={
                "server_settings": {
                    "application_name": "iac-scan-doc"
                }
            }

DATABASE_URL = config.DATABASE_URL
DATABASE_URL_PDF = config.DATABASE_URL_PDF
DATABASE_URL_GROUP_DOC = config.DATABASE_URL_PDF

engine = create_async_engine(DATABASE_URL, connect_args=connect_args)
engine_pdf = create_async_engine(DATABASE_URL_PDF, connect_args=connect_args)
engine_group_doc = create_async_engine(DATABASE_URL_GROUP_DOC, connect_args=connect_args)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
async_session_maker_pdf = async_sessionmaker(engine_pdf, expire_on_commit=False)
async_session_maker_group_doc = async_sessionmaker(engine_group_doc, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


async def get_session_pdf() -> AsyncSession:
    async with async_session_maker_pdf() as session:
        yield session


async def get_session_group_doc() -> AsyncSession:
    async with async_session_maker_group_doc() as session:
        yield session
