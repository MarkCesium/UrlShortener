from msgspec import Struct

class Index(Struct):
    name: str
    author: str
    repository: str
    debug: bool
    swagger: str | None
