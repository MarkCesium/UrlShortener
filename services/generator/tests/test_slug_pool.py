import pytest
from fakeredis import aioredis

from src.core.exceptions import PoolExhaustedError
from src.core.services.slug import get_slug, is_pool_full, refill_pool


async def test_refill_pool_adds_slugs(redis: aioredis.FakeRedis) -> None:
    assert await redis.scard("slug") == 0
    await refill_pool(redis)
    assert await redis.scard("slug") > 0


async def test_is_pool_full_when_empty(redis: aioredis.FakeRedis) -> None:
    assert await is_pool_full(redis) is False


async def test_is_pool_full_when_filled(redis: aioredis.FakeRedis) -> None:
    for i in range(1000):
        await redis.sadd("slug", f"slug{i:04d}")
    assert await is_pool_full(redis) is True


async def test_get_slug_returns_string(redis: aioredis.FakeRedis) -> None:
    await redis.sadd("slug", "abc123")
    slug = await get_slug(redis)
    assert slug == "abc123"
    assert isinstance(slug, str)


async def test_get_slug_removes_from_pool(redis: aioredis.FakeRedis) -> None:
    await redis.sadd("slug", "abc123")
    await get_slug(redis)
    assert await redis.scard("slug") == 0


async def test_get_slug_raises_when_pool_empty(redis: aioredis.FakeRedis) -> None:
    with pytest.raises(PoolExhaustedError):
        await get_slug(redis)
