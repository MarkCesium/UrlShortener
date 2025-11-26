from faststream.nats import NatsBroker

from src.core.config import settings

__all__ = ("init_broker", "get_broker_client", "stop_broker")

broker: NatsBroker | None = None


async def init_broker() -> None:
    global broker
    if broker is None:
        broker = NatsBroker(servers=settings.broker.url)
        await broker.start()


async def get_broker_client() -> NatsBroker:
    global broker
    if broker is None:
        raise RuntimeError("Broker not initialized. Call init_broker() first.")
    return broker


async def stop_broker() -> None:
    global broker
    if broker is not None:
        await broker.stop()
