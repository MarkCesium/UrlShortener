import orjson
from faststream.nats import NatsBroker
from msgspec import Struct


class Slug(Struct):
    slug: str


class BrokerService:
    def __init__(self, broker: NatsBroker):
        self.broker = broker

    async def get_slug(self) -> str:
        msg = await self.broker.request(None, "get.slug")
        schema = Slug(**orjson.loads(msg.body))
        return schema.slug
