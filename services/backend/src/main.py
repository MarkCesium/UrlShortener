from litestar import Litestar

from src.api.controllers.url import URLController
from src.infra.database import get_db_plugin
from src.core.config import settings

app = Litestar(
    route_handlers=[
        URLController,
    ],
    plugins=[get_db_plugin(settings.database)],
)
