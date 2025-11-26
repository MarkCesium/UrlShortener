from litestar import Controller, get, post
from litestar.response import Redirect


class URLController(Controller):
    @get("/{slug:str}}")
    async def redirect(self, slug: str) -> Redirect:
        return Redirect("")

    @post("/")
    async def create(self): ...
