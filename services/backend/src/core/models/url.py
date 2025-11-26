from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from advanced_alchemy.base import BigIntAuditBase


class URL(BigIntAuditBase):
    __tablename__ = "urls"

    slug: Mapped[str] = mapped_column(
        String(6),
        unique=True,
        nullable=False,
        index=True,
    )

    original_url: Mapped[str] = mapped_column(
        String(2048),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )
