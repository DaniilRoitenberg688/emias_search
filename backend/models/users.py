import uuid
from typing import Optional

from pydantic import BaseModel
from enum import Enum

class TypeOfUsers(str, Enum):
    all_users = 'all_users'
    hospitalized = 'hospitalized'
    applicants = 'applicants'


class UserOut(BaseModel):
    fio: str
    mdoc_id: uuid.UUID
    ib_num: str
    pacs_uid: Optional[str]
