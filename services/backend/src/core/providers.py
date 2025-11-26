from typing import Annotated

from advanced_alchemy.extensions.litestar import providers
from litestar.datastructures import State
from litestar.di import Provide
from faststream.nats import NatsBroker

from src.core.services.url import URLService
from src.core.services.broker import BrokerService

async def get_broker(state: State) -> NatsBroker:
    return state.broker

get_url_service = providers.create_service_provider(URLService)

async def get_broker_service(broker: Annotated[NatsBroker, Provide(get_broker)]) -> BrokerService:
    return BrokerService(broker)