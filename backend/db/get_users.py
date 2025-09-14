import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from db.engine import get_session
from models import TypeOfUsers


async def get_users(session: AsyncSession, limit, offset, type_of_users: TypeOfUsers, dept_id: str):
    data = ""
    if type_of_users == TypeOfUsers.all_users:
        with open("db/sql_requests/get_all_users_request", "r") as file:
            # LIMIT {} OFFSET {}
            data = file.read()
    if type_of_users == TypeOfUsers.hospitalized:
        with open("db/sql_requests/get_hospitalized_request", "r") as file:
            # LIMIT {} OFFSET {}
            data = file.read()
            data = data.format(dept_id=dept_id)
    if type_of_users == TypeOfUsers.applicants:
        with open("db/sql_requests/get_applicants_request", "r") as file:
            # LIMIT {} OFFSET {}
            data = file.read()
            data = data.format(dept_id=dept_id)
    data += "\n"
    if limit:
        data += f"LIMIT {limit} "
    if offset:
        data += f"OFFSET {offset}"
    query = text(data)

    request = await session.execute(query)

    return request

#
# if __name__ == '__main__':
#     session = get_session()
#     asyncio.run(get_users(session=session))
