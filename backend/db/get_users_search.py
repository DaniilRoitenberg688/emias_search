from click import command

from db.engine import get_session
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text


async def get_users_search(session: AsyncSession, limit, offset, line):
    with open('db/sql_requests/get_users_search_request', 'r') as file:
        # LIMIT {} OFFSET {}
        data = file.read()
        data += '\n'
        if limit:
            data += f'LIMIT {limit} '
        if offset:
            data += f'OFFSET {offset}'
        print(line)
        # WHERE md.surname LIKE '%{line}%' OR md.name LIKE '%{line}%' OR md.patron LIKE '%{line}%'

        search_fields = line.split()
        print(search_fields)
        if len(search_fields) == 1:
            command = "\nWHERE md.surname LIKE '%{line}%' OR md.name LIKE '%{line}%' OR md.patron LIKE '%{line}%'".format(
                line=search_fields[0])
        elif len(search_fields) == 2:
            command = "\nWHERE md.surname LIKE '%{line1}%' AND md.name LIKE '%{line2}%' OR md.name LIKE '%{line1}%' AND md.patron LIKE '%{line2}%' OR md.surname LIKE '%{line1}%' AND md.patron LIKE '%{line2}%' OR md.surname LIKE '%{line2}%' AND md.name LIKE '%{line1}%' OR md.name LIKE '%{line2}%' AND md.patron LIKE '%{line1}%' OR md.surname LIKE '%{line2}%' AND md.patron LIKE '%{line1}%'".format(
                line1=search_fields[0], line2=search_fields[1])
            # command = "\nWHERE md.surname LIKE '%{line1}%' AND md.name LIKE '%{line2}%'".format(line1=search_fields[0], line2=search_fields[1])

        elif len(search_fields) == 3:
            command = "\nWHERE (md.surname LIKE '{line1}' AND md.name LIKE '{line2}' AND md.patron LIKE '{line3}') OR (md.surname LIKE '{line1}' AND md.name LIKE '{line3}' AND md.patron LIKE '{line2}') OR (md.surname LIKE '{line2}' AND md.name LIKE '{line1}' AND md.patron LIKE '{line3}') OR (md.surname LIKE '{line2}' AND md.name LIKE '{line3}' AND md.patron LIKE '{line1}') OR (md.surname LIKE '{line3}' AND md.name LIKE '{line1}' AND md.patron LIKE '{line2}') OR (md.surname LIKE '{line3}' AND md.name LIKE '{line2}' AND md.patron LIKE '{line1}')".format(
                line1=search_fields[0], line2=search_fields[1], line3=search_fields[2])

        else:
            return []

        data = data.format(search_command=command)

        query = text(data)

    request = await session.execute(query)

    return request


if __name__ == '__main__':
    session = get_session()
    asyncio.run(get_users_search(session=session, line='kk', limit=10, offset=0))
