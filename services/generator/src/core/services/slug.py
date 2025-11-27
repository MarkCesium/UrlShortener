import asyncio
import string
import secrets
import logging

from redis.asyncio import Redis

from src.core.config import settings

logger = logging.getLogger(__name__)


class SlugGenerator:
    _alphabet = string.ascii_letters + string.digits

    @classmethod
    def generate(cls) -> str:
        return "".join(secrets.choice(cls._alphabet) for _ in range(6))


async def is_pool_full(redis: Redis) -> bool:
    size = await redis.scard("slug")  # type: ignore
    return size >= settings.redis.pool_size


async def refill_pool(redis: Redis) -> None:
    for _ in range(settings.redis.batch_size):
        await redis.sadd("slug", SlugGenerator.generate())  # type: ignore


async def get_slug(redis: Redis) -> str:
    slug: bytes = await redis.spop("slug")  # type: ignore
    if not await is_pool_full(redis):
        asyncio.create_task(refill_pool(redis))

    return slug.decode()
