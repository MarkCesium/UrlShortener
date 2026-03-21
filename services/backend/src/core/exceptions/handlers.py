from typing import Any

from litestar import Request, Response

from src.core.exceptions.base import AppError


def app_exception_handler(_: Request[Any, Any, Any], exc: AppError) -> Response[Any]:
    return Response(
        content={"detail": exc.detail},
        status_code=exc.status_code,
    )
