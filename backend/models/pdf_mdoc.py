import uuid
from collections.abc import Sequence
from pydantic import BaseModel


class PdfMdocModel(BaseModel):
    mdoc_id: uuid.UUID
    group_doc_id: int
    data: bytes

