from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_users_data, get_users_search
from db.engine import get_session
from models import TypeOfUsers, UserOut

user_router = APIRouter(prefix="/users",
                        tags=['users'])


@user_router.get("", response_model=list[UserOut], status_code=200)
async def get_all(
    dept_id: str,
    session: AsyncSession = Depends(get_session),
    offset: int | None = None,
    limit: int | None = None,
    type_of_users: TypeOfUsers = TypeOfUsers.all_users,
):
    users = await get_users_data(
        session, offset=offset, limit=limit, type_of_users=type_of_users, dept_id=dept_id
    )
    return [UserOut(fio=i.fio, ib_num=i.ib_num, mdoc_id=i.mdoc_id) for i in users]


@user_router.get("/search", response_model=list[UserOut], status_code=200)
async def get_with_search(
    search_line: str,
    dept_id: str,
    session: AsyncSession = Depends(get_session),
    offset: int | None = None,
    limit: int | None = None,
    type_of_users: TypeOfUsers = TypeOfUsers.all_users,
):
    users = await get_users_search(
        session=session,
        limit=limit,
        offset=offset,
        line=search_line.upper(),
        type_of_users=type_of_users,
        dept_id=dept_id
    )
    return [UserOut(fio=i.fio, ib_num=i.ib_num, mdoc_id=i.mdoc_id) for i in users]
