from fastapi import APIRouter
from models import UserOut
from db import get_users_data
from fastapi import Depends
from db.engine import get_session
from sqlalchemy.ext.asyncio import AsyncSession

user_router = APIRouter(prefix='/users')


@user_router.get('', response_model=list[UserOut], status_code=200)
async def get_all(session: AsyncSession=Depends(get_session), offset: int | None = None, limit: int | None = None):
    users: list = await get_users_data(session, offset=offset, limit=limit)
    return [UserOut(fio=i.fio, ib_num=i.ib_num) for i in users]