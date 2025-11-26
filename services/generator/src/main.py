import asyncio

from faststream import FastStream
from faststream.nats import NatsBroker

from src.handlers.slug import router as slug_router
from src.core.config import settings


async def main():
    broker = NatsBroker(settings.broker.url)
    app = FastStream(broker)
    broker.include_router(slug_router)
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
