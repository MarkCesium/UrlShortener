import logging

from litestar import Controller, get, post, status_codes
from litestar.di import Provide
from litestar.response import Redirect
from sqlalchemy.exc import IntegrityError

from src.api.schemas.url import URLCreate, URLRead
from src.core.exceptions import AppError, ConflictError, NotFoundError
from src.core.models.url import URL
from src.core.providers import get_broker_service, get_url_service
from src.core.services.broker import BrokerService
from src.core.services.url import URLService

logger = logging.getLogger(__name__)

MAX_SLUG_RETRIES = 3


class URLController(Controller):
    dependencies = {
        "broker": Provide(get_broker_service),
        "service": Provide(get_url_service),
    }

    @get("/{slug:str}")
    async def redirect(self, slug: str, service: URLService) -> Redirect:
        url = await service.get_one_or_none(URL.slug == slug)
        if url is None:
            raise NotFoundError(f"URL with slug: {slug} not found")
        return Redirect(url.original_url, status_code=status_codes.HTTP_302_FOUND)

    @post("/shorten")
    async def create(self, data: URLCreate, service: URLService, broker: BrokerService) -> URLRead:
        if data.slug is not None:
            if await service.get_one_or_none(URL.slug == data.slug) is not None:
                raise ConflictError(f"URL with slug: {data.slug} already exists")
            entity = await service.create(data)
            return service.to_schema(entity, schema_type=URLRead)

        for attempt in range(MAX_SLUG_RETRIES):
            data.slug = await broker.get_slug()
            try:
                entity = await service.create(data)
                return service.to_schema(entity, schema_type=URLRead)
            except IntegrityError:
                logger.warning(
                    "Slug collision on '%s', retrying (%d/%d)",
                    data.slug,
                    attempt + 1,
                    MAX_SLUG_RETRIES,
                )

        raise AppError("Failed to generate a unique slug")
