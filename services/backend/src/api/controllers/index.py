from litestar import get

from src.api.schemas.index import Index
from src.core.config import settings

@get("/")
async def index() -> Index:
    return Index(
        name="Url Shortener",
        author="MarkCesium",
        repository="https://github.com/MarkCesium/UrlShortener",
        debug=settings.app.debug,
        swagger=settings.app.domain + "/schema" if settings.app.debug else None
    )
    