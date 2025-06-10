import uuid

from pydantic import BaseModel


class UserOut(BaseModel):
    fio: str
    mdoc_id: uuid.UUID
    ib_num: str
