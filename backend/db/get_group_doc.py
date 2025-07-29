from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text



async def get_group_doc(session: AsyncSession):

    request = 'select id, name from doc.group_doc where is_actual'
    
    result = await session.execute(text(request))

    return result
