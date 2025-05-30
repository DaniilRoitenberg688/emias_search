from pydantic import BaseModel

class UserOut(BaseModel):
    fio: str
    ib_num: str
