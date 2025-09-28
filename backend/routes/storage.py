from fastapi import APIRouter


from storage import redis
from config import config
import uuid

storage_router = APIRouter(prefix="/storage", tags=["storage"])


@storage_router.get("", status_code=200)
async def get_token(id: str) -> str | None:
    print(id)
    token = await redis.get(id)
    
    return token


@storage_router.post("", status_code=201)
async def set_token(token: str) -> str:
    id = uuid.uuid4()
    print(id)
    print(type(float(config.SESSION_TIME)))
    await redis.setex(str(id), int(config.SESSION_TIME), token)
    return str(id)

@storage_router.delete("")
async def delete_token(id: str):
    await redis.delete(id)
    
