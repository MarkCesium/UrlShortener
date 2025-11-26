from faststream.nats import NatsRouter
from msgspec.json import encode

from src.core.providers import SlugServiceDep
from src.schemas.slug import Slug

router = NatsRouter(prefix="slug.")


@router.subscriber("get")
async def generate_slug(slug_service: SlugServiceDep) -> bytes:
    response = Slug(slug=slug_service.generate())
    return encode(response)
