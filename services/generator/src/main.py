from faststream import FastStream
from faststream.nats import NatsBroker

from src.handlers.slug import router as slug_router

broker = NatsBroker("nats://localhost:4222")
broker.include_router(slug_router)
app = FastStream(broker)
