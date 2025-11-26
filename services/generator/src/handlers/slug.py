from faststream.nats import NatsRouter

from src.core.providers import SlugServiceDep

router = NatsRouter(prefix="slug.")


@router.subscriber("generate")
async def generate_slug(slug_service: SlugServiceDep) -> str:
    return slug_service.generate()
