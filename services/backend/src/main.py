import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from litestar import Litestar

from src.core.config import settings
from src.core.exceptions.base import AppError
from src.core.exceptions.handlers import app_exception_handler
from src.infra.broker import init_broker, stop_broker
from src.infra.database import database_plugin


@asynccontextmanager
async def lifespan(app: Litestar) -> AsyncGenerator[None]:
    logging.basicConfig(
        level=settings.logging.level_value,
        format=settings.logging.format,
        datefmt=settings.logging.date_format,
    )
    await init_broker()
    yield
    await stop_broker()


def create_app() -> Litestar:
    from litestar.openapi.config import OpenAPIConfig
    from litestar.openapi.plugins import SwaggerRenderPlugin

    from src.api.controllers.index import index
    from src.api.controllers.url import URLController

    return Litestar(
        debug=settings.app.debug,
        route_handlers=[index, URLController],
        plugins=[database_plugin],
        lifespan=[lifespan],
        exception_handlers={
            AppError: app_exception_handler,
        },
        openapi_config=OpenAPIConfig(
            title="URL Shortener",
            description="URL Shortener API",
            version="0.1.0",
            render_plugins=[SwaggerRenderPlugin()],
        ),
    )


app = create_app()
