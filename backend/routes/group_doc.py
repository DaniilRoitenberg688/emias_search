from fastapi import APIRouter, Depends
from db.engine import get_session_group_doc
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_group_doc as get_group_doc_request
from pydantic import BaseModel

class GroupDoc(BaseModel):
    id: int
    name: str

router = APIRouter(prefix='/group_doc', tags=['group doc'])


@router.get('', response_model=list[GroupDoc], status_code=200)
async def get_group_doc(
        session: AsyncSession = Depends(get_session_group_doc)
):
    result = await get_group_doc_request(session=session)
    return [GroupDoc(id=i.id, name=i.name) for i in result]

