import redis.asyncio as redis
from app.core.config import settings

async_redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    decode_responses=True,
)


