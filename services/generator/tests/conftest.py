import pytest
from fakeredis import aioredis


@pytest.fixture
async def redis() -> aioredis.FakeRedis:
    client = aioredis.FakeRedis()
    yield client
    await client.aclose()
