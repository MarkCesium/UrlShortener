import asyncio
import logging
import secrets
import string

from redis.asyncio import Redis

from src.core.config import settings
from src.core.exceptions import PoolExhaustedError

logger = logging.getLogger(__name__)


class SlugGenerator:
    _alphabet = string.ascii_letters + string.digits

    @classmethod
    def generate(cls) -> str:
        return "".join(secrets.choice(cls._alphabet) for _ in range(6))


async def is_pool_full(redis: Redis) -> bool:
    size: int = await redis.scard("slug")  # type: ignore[misc]
    return size >= settings.redis.pool_size


async def refill_pool(redis: Redis) -> None:
    logger.info("Refilling slug pool with %d slugs", settings.redis.batch_size)
    for _ in range(settings.redis.batch_size):
        await redis.sadd("slug", SlugGenerator.generate())  # type: ignore
    logger.info("Slug pool refilled")


async def get_slug(redis: Redis) -> str:
    slug: bytes | None = await redis.spop("slug")  # type: ignore
    if slug is None:
        raise PoolExhaustedError

    if not await is_pool_full(redis):
        asyncio.create_task(refill_pool(redis))

    return slug.decode()
