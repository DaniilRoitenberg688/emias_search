from fastapi import APIRouter
from models import UserOut
from db import get_users_data
from fastapi import Depends
from db.engine import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_users_search

user_router = APIRouter(prefix='/users')


@user_router.get('', response_model=list[UserOut], status_code=200)
async def get_all(session: AsyncSession = Depends(get_session), offset: int | None = None, limit: int | None = None):
    users: list = await get_users_data(session, offset=offset, limit=limit)
    return [UserOut(fio=i.fio, ib_num=i.ib_num, mdoc_id=i.mdoc_id) for i in users]


@user_router.get('/search', response_model=list[UserOut], status_code=200)
async def get_with_search(search_line: str, session: AsyncSession = Depends(get_session), offset: int | None = None,
                          limit: int | None = None):
    users: list = await get_users_search(session=session, limit=limit, offset=offset, line=search_line.upper())
    return [UserOut(fio=i.fio, ib_num=i.ib_num, mdoc_id=i.mdoc_id) for i in users]
