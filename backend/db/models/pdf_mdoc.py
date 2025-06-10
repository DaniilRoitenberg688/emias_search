from db.engine import Base
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, DateTime, BINARY, String, UUID, text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from config import config
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime



class PdfMdoc(Base):
    __tablename__ = 'pdf_mdoc'
    __table_args__ = {'schema': 'ext'}
    id: Mapped[int] = mapped_column(UUID, primary_key=True, nullable=True, server_default=text("uuid_generate_v1()"))
    mdoc_id: Mapped[str] = mapped_column(UUID, nullable=False)
    pdf_data: Mapped[bytes] = mapped_column(BINARY)
