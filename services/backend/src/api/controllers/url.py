from litestar import Controller, get, post, status_codes
from litestar.exceptions.http_exceptions import NotFoundException, HTTPException
from litestar.di import Provide
from litestar.response import Redirect

from src.api.schemas.url import URLCreate, URLRead
from src.core.models.url import URL
from src.core.services.broker import BrokerService
from src.core.services.url import URLService
from src.core.providers import get_broker_service, get_url_service


class URLController(Controller):
    dependencies = {
        "broker": Provide(get_broker_service),
        "service": Provide(get_url_service)
    }
    
    @get("/{slug:str}}")
    async def redirect(self, slug: str, service: URLService) -> Redirect:
        url = await service.get_one_or_none(URL.slug == slug)
        if url is None:
            raise NotFoundException(f"URL with slug: {slug} not found")
        return Redirect(url.original_url, status_code=status_codes.HTTP_302_FOUND)

    @post("/")
    async def create(self, data: URLCreate, service: URLService, broker: BrokerService) -> URLRead:
        if data.slug is None:
            data.slug = await broker.get_slug()
        else:
            if await service.get_one_or_none(URL.slug == data.slug) is not None: 
                raise HTTPException(status_code=status_codes.HTTP_409_CONFLICT, detail=f"URL with slug: {data.slug} already exists")
        entity = await service.create(data)
        return service.to_schema(entity, schema_type=URLRead)
    