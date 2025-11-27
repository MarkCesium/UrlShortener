from faststream.nats import NatsRouter
from msgspec.json import encode

from src.core.providers import SlugDep
from src.schemas.slug import Slug

router = NatsRouter(prefix="slug.")


@router.subscriber("get")
async def generate_slug(slug: SlugDep) -> bytes:
    response = Slug(slug)
    return encode(response)
