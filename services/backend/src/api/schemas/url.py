from typing import Annotated
from datetime import datetime
from msgspec import Struct, Meta

Slug = Annotated[str, Meta(min_length=6, max_length=18)]


class URLBase(Struct):
    original_url: str


class URLCreate(URLBase):
    slug: Slug | None = None


class URLRead(URLBase):
    id: int
    slug: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
