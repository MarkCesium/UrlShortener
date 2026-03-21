from collections.abc import AsyncGenerator

import pytest
from fakeredis import aioredis


@pytest.fixture
async def redis() -> AsyncGenerator[aioredis.FakeRedis]:
    client = aioredis.FakeRedis()
    yield client
    await client.aclose()
