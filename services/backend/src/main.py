from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from litestar import Litestar

from src.infra.broker import init_broker, stop_broker
from src.infra.database import database_plugin

@asynccontextmanager
async def lifespan(app: Litestar) -> AsyncGenerator[None, None]:
    await init_broker()
    yield
    await stop_broker()

def create_app() -> Litestar:
    from src.api.controllers.url import URLController
    from src.core.config import settings
    from litestar.openapi.config import OpenAPIConfig
    from litestar.openapi.plugins import SwaggerRenderPlugin

    return Litestar(
        debug=settings.app.debug,
        route_handlers=[URLController],
        plugins=[database_plugin],
        lifespan=[lifespan],
        openapi_config=OpenAPIConfig(
            title="Litestar Example",
            description="Example of litestar",
            version="0.0.1",
            render_plugins=[SwaggerRenderPlugin()],
        ),
    )

app = create_app()
