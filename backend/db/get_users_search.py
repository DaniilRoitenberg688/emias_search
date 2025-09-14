from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from db.engine import get_session
from models.users import TypeOfUsers


async def get_users_search(session: AsyncSession, limit, offset, line, type_of_users: TypeOfUsers, dept_id):
    data = ''
    if type_of_users == TypeOfUsers.all_users:
        with open('db/sql_requests/get_all_users_search_request', 'r') as file:
            # LIMIT {} OFFSET {}
            data = file.read()

    if type_of_users == TypeOfUsers.hospitalized:
        with open("db/sql_requests/get_hospitalized_search_request", "r") as file:
            # LIMIT {} OFFSET {}
            data = file.read()
    if type_of_users == TypeOfUsers.applicants:
        with open("db/sql_requests/get_applicants_search_request", "r") as file:
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
        if not line.isdigit():
            if '-' in line:
                if line.count('-') == 4:
                    command = "\n AND f.people_id = '{people_id}'".format(people_id=line)
                else:
                    command = "\nAND mm.mdoc_get_num_format(hd.admission_num,hd.admission_year,md.num_org,md.num_filial,md.num_type,mdtp.id,mdtp.class, data) LIKE '{line}%'".format(
                    line=search_fields[0])
            else:
                command = "\nAND (md.surname LIKE '%{line}%' OR md.name LIKE '%{line}%' OR md.patron LIKE '%{line}%')".format(
                    line=search_fields[0])
        else:
            command = "\nAND mm.mdoc_get_num_format(hd.admission_num,hd.admission_year,md.num_org,md.num_filial,md.num_type,mdtp.id,mdtp.class, data) LIKE '{line}%' OR md.surname LIKE '%{line}%' OR md.name LIKE '%{line}%' OR md.patron LIKE '%{line}%'".format(
                line=search_fields[0])



    elif len(search_fields) == 2:
        command = "\nAND md.surname LIKE '%{line1}%' AND md.name LIKE '%{line2}%' OR md.name LIKE '%{line1}%' AND md.patron LIKE '%{line2}%' OR md.surname LIKE '%{line1}%' AND md.patron LIKE '%{line2}%' OR md.surname LIKE '%{line2}%' AND md.name LIKE '%{line1}%' OR md.name LIKE '%{line2}%' AND md.patron LIKE '%{line1}%' OR md.surname LIKE '%{line2}%' AND md.patron LIKE '%{line1}%'".format(
            line1=search_fields[0], line2=search_fields[1])
        # command = "\nWHERE md.surname LIKE '%{line1}%' AND md.name LIKE '%{line2}%'".format(line1=search_fields[0], line2=search_fields[1])

    elif len(search_fields) == 3:
        command = "\nAND (md.surname LIKE '%{line1}%' AND md.name LIKE '%{line2}%' AND md.patron LIKE '%{line3}%') OR (md.surname LIKE '%{line1}' AND md.name LIKE '%{line3}%' AND md.patron LIKE '%{line2}%') OR (md.surname LIKE '%{line2}%' AND md.name LIKE '%{line1}%' AND md.patron LIKE '%{line3}%') OR (md.surname LIKE '%{line2}%' AND md.name LIKE '%{line3}%' AND md.patron LIKE '%{line1}%') OR (md.surname LIKE '%{line3}%' AND md.name LIKE '%{line1}%' AND md.patron LIKE '%{line2}%') OR (md.surname LIKE '%{line3}%' AND md.name LIKE '%{line2}%' AND md.patron LIKE '%{line1}%')".format(
            line1=search_fields[0], line2=search_fields[1], line3=search_fields[2])

    else:
        return []
    if type_of_users == TypeOfUsers.applicants or type_of_users == TypeOfUsers.hospitalized:
        data = data.format(search_command=command, dept_id=dept_id)
    else:
        data = data.format(search_command=command)

    query = text(data)

    request = await session.execute(query)

    return request


# if __name__ == '__main__':
#     session = get_session()
#     asyncio.run(get_users_search(session=session, line='kk', limit=10, offset=0))
