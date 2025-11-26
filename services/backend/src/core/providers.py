from advanced_alchemy.extensions.litestar import providers

from src.core.services.url import URLService
from src.core.services.broker import BrokerService

from src.infra.broker import get_broker_client


get_url_service = providers.create_service_provider(URLService)


async def get_broker_service() -> BrokerService:
    broker = await get_broker_client()
    return BrokerService(broker)
