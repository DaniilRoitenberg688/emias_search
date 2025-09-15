# import asyncio
# from db.engine import get_session

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from models import TypeOfUsers


async def get_users(session: AsyncSession, limit, offset, type_of_users: TypeOfUsers, dept_id: str):

    params = {"limit": limit, "offset": offset}

    if type_of_users == TypeOfUsers.all_users:
        with open("db/sql_requests/get_all_users_request.sql", "r") as file:
            data = file.read()
    if type_of_users == TypeOfUsers.hospitalized:
        with open("db/sql_requests/get_hospitalized_request.sql", "r") as file:
            data = file.read()
            params.update({"dept_id": dept_id})
    if type_of_users == TypeOfUsers.applicants:
        with open("db/sql_requests/get_applicants_request.sql", "r") as file:
            data = file.read()
            params.update({"dept_id": dept_id})

    query = text(data)

    request = await session.execute(query, params)

    return request

#
# if __name__ == '__main__':
#     session = get_session()
#     asyncio.run(get_users(session=session))
