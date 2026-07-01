import redis.asyncio as redis

from app.core.config import settings

_redis_client: redis.Redis | None = None


def get_redis() -> redis.Redis:
    """Single shared point for obtaining the async Redis client.

    Mocked in tests (e.g. via fakeredis) by patching this function
    where it is imported/used, e.g. app.bot.handlers.get_redis.
    """
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis_client
