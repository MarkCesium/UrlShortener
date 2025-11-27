import asyncio
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from faststream import FastStream
from faststream.nats import NatsBroker

from src.handlers.slug import router as slug_router
from src.core.config import settings
from src.core.services.slug import is_pool_full, refill_pool
from src.infra.redis import init_redis, get_redis, close_redis


@asynccontextmanager
async def lifespan() -> AsyncGenerator[None, None]:
    await init_redis()
    redis = await get_redis()
    if not await is_pool_full(redis):
        await refill_pool(redis)
    yield

    await close_redis()


async def main():
    broker = NatsBroker(settings.broker.url)
    app = FastStream(broker, lifespan=lifespan)
    broker.include_router(slug_router)
    await app.run(log_level=settings.logging.level_value)


if __name__ == "__main__":
    asyncio.run(main())
