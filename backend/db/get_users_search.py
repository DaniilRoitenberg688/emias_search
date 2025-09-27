# from db.engine import get_session
import re

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from models.users import TypeOfUsers

async def get_users_search(session: AsyncSession, limit:int, offset:int, line:str, type_of_users: TypeOfUsers, dept_id:str):
    params: dict[str, str|int] = {"limit": limit, "offset": offset}

    res = []

    if type_of_users == TypeOfUsers.all_users:
        with open('db/sql_requests/get_all_users_search_request.sql', 'r') as file:
            data = file.read()

    if type_of_users == TypeOfUsers.hospitalized:
        with open("db/sql_requests/get_hospitalized_search_request.sql", "r") as file:
            data = file.read()
        params.update({"dept_id": dept_id})

    if type_of_users == TypeOfUsers.applicants:
        with open("db/sql_requests/get_applicants_search_request.sql", "r") as file:
            data = file.read()
        params.update({"dept_id": dept_id})

    # TODO: Разобраться с логикой. Вроде накидал пример нового поиска, но не успел всё сделать.
    if line.strip():
        if re.search(r"^[A-Za-zА-Яа-я]+(?:\s+[A-Za-zА-Яа-я]+)*", line):
            command = "\n AND to_tsvector('russian', md.surname || ' ' || md.name || ' ' || md.patron) @@ plainto_tsquery(:search_field)"
            params.update({'search_field': line})
        else:
            command = "\n AND f.pacs_uid LIKE :search_field"
            params.update({'search_field': f'%{line}%'})

            command_2 = "\n AND f.pacs_uid LIKE :search_field"

    search_field = re.sub(r"[.,!@#\-\s_]", "", line)
    if search_field:
        if search_field.isdigit():
            command = "\n AND (f.pacs_uid LIKE :search_field or mm.mdoc_get_num_format(md.num, md.year,md.num_org,md.num_filial,md.num_type,mdtp.id,mdtp.class, data) LIKE :search_field)"
            params.update({'search_field': f'%{line}%'})
        else:
            command = "\n AND (to_tsvector('russian', md.surname || ' ' || md.name || ' ' || md.patron) @@ plainto_tsquery(:search_field) or mm.mdoc_get_num_format(md.num, md.year, md.num_org,md.num_filial,md.num_type,mdtp.id,mdtp.class, data) LIKE :o_search_field)"
            params.update({'search_field': line, 'o_search_field': f'%{line}%'})

    else:
        return []

    data = data.format(search_command=command)
    query = text(data)
    request = await session.execute(query, params)
    return request


# if __name__ == '__main__':
#     session = get_session()
#     asyncio.run(get_users_search(session=session, line='kk', limit=10, offset=0))
