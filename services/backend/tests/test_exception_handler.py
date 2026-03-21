from unittest.mock import MagicMock

from src.core.exceptions import NotFoundError
from src.core.exceptions.handlers import app_exception_handler


def test_handler_returns_correct_status_and_body() -> None:
    exc = NotFoundError("not found")
    request = MagicMock()

    response = app_exception_handler(request, exc)

    assert response.status_code == 404
    assert response.content == {"detail": "not found"}
