from datetime import datetime

from sqlalchemy import Integer, Date, BINARY, String, UUID, text
from sqlalchemy.orm import Mapped, mapped_column

from config import config
from db.engine import Base


class PdfMdoc(Base):
    __tablename__ = config.TABLE_NAME_PDF
    __table_args__ = {'schema': config.TABLE_SCHEMA_PDF}
    id: Mapped[int] = mapped_column(UUID, primary_key=True, nullable=True, server_default=text("uuid_generate_v1()"))
    mdoc_id: Mapped[str] = mapped_column(UUID, nullable=False)
    pdf_data: Mapped[bytes] = mapped_column(BINARY)
    group_doc_id: Mapped[int] = mapped_column(Integer)
    doc_name: Mapped[str] = mapped_column(String)
    create_dt: Mapped[datetime] = mapped_column(Date, default=datetime.now())
