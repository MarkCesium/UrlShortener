from unittest.mock import AsyncMock, MagicMock

import pytest
from msgspec import Struct, json

from src.core.exceptions import AppError
from src.core.services.broker import BrokerService


class SlugResponse(Struct):
    slug: str


@pytest.fixture
def mock_nats_broker() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def broker_service(mock_nats_broker: AsyncMock) -> BrokerService:
    return BrokerService(mock_nats_broker)


async def test_get_slug_returns_decoded_slug(
    broker_service: BrokerService,
    mock_nats_broker: AsyncMock,
) -> None:
    msg = MagicMock()
    msg.body = json.encode(SlugResponse(slug="abc123"))
    mock_nats_broker.request.return_value = msg

    result = await broker_service.get_slug()

    assert result == "abc123"
    mock_nats_broker.request.assert_awaited_once_with(None, "slug.get")


async def test_get_slug_raises_app_error_on_failure(
    broker_service: BrokerService,
    mock_nats_broker: AsyncMock,
) -> None:
    mock_nats_broker.request.side_effect = TimeoutError("no response")

    with pytest.raises(AppError, match="Failed to generate slug"):
        await broker_service.get_slug()
