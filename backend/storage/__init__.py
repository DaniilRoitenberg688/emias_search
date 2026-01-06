from redis.asyncio import Redis
from redis.asyncio.sentinel import Sentinel

from config import config

sentinel = Sentinel(
    [(config.REDIS_SENTINEL_HOST, config.REDIS_SENTINEL_PORT)],
    sentinel_kwargs={"password": config.REDIS_SENTINEL_PASSWORD},
    password=config.REDIS_SENTINEL_PASSWORD,
    socket_timeout=float(config.REDIS_TIMEOUT),
)
##### Раскоментировать при работе в проде
# redis = sentinel.master_for(
#     service_name=config.REDIS_SENTINEL_MASTER,
#     decode_responses=True,
# )

redis = Redis(host=str(config.REDIS_HOST), port=6379, decode_responses=True)
