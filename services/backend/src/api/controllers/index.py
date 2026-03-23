from litestar import get
from litestar.response import Template

from src.core.config import settings


@get("/", include_in_schema=False)
async def index() -> Template:
    return Template(template_name="index.html", context={"domain": settings.app.domain})
