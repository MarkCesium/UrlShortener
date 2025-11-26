from typing import Annotated

from faststream import Depends

from src.core.services.slug import SlugService


async def get_slug_service() -> SlugService:
    return SlugService()


SlugServiceDep = Annotated[SlugService, Depends(get_slug_service)]
