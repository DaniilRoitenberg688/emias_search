from db.engine import get_session
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

async def get_users(session: AsyncSession, limit=10, offset=0):


    with open('db/sql_requests/get_users_request', 'r') as file:
        query = text(file.read().format(limit, offset))


    request = await session.execute(query)


    return request



if __name__ == '__main__':
    session = get_session()
    asyncio.run(get_users(session=session))




