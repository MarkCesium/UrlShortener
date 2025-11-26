from faststream.nats import NatsBroker

from src.core.config import settings

broker = NatsBroker(
    servers=settings.broker.url,
)
