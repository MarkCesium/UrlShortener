import logging

from faststream.nats import NatsBroker
from msgspec import Struct, json

from src.core.exceptions import AppError

logger = logging.getLogger(__name__)


class Slug(Struct):
    slug: str


class BrokerService:
    def __init__(self, broker: NatsBroker):
        self.broker = broker

    async def get_slug(self) -> str:
        try:
            msg = await self.broker.request(None, "slug.get")
            schema = json.decode(msg.body, type=Slug)
            return schema.slug
        except Exception as e:
            logger.exception("Failed to get slug from generator")
            raise AppError("Failed to generate slug") from e
