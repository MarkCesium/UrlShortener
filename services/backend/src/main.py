from litestar import Litestar

from src.api.controllers.url import URLController
from src.infra.broker import broker
from src.infra.database import get_db_plugin
from src.core.config import settings

async def startup(app: Litestar):
    await broker.start()
    app.state.broker

async def shutdown(app: Litestar):
    await broker.stop()

app = Litestar(
    route_handlers=[
        URLController,
    ],
    plugins=[get_db_plugin(settings.database)],
    on_startup=[startup],
    on_shutdown=[shutdown],
)
