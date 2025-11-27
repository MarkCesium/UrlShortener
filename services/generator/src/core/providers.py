from typing import Annotated

from faststream import Depends
from redis.asyncio import Redis

from src.core.services.slug import get_slug
from src.infra.redis import get_redis


async def get_slug_dep(redis: Redis = Depends(get_redis)) -> str:
    return await get_slug(redis)


SlugDep = Annotated[str, Depends(get_slug_dep)]
