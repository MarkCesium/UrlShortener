from src.core.exceptions import AppError, ConflictError, NotFoundError


class TestAppError:
    def test_default_values(self) -> None:
        err = AppError()
        assert err.status_code == 500
        assert err.detail == "Internal server error"

    def test_custom_values(self) -> None:
        err = AppError(detail="oops", status_code=503)
        assert err.status_code == 503
        assert err.detail == "oops"
        assert str(err) == "oops"


class TestNotFoundError:
    def test_default_values(self) -> None:
        err = NotFoundError()
        assert err.status_code == 404
        assert err.detail == "Resource not found"

    def test_custom_detail(self) -> None:
        err = NotFoundError("slug xyz not found")
        assert err.status_code == 404
        assert err.detail == "slug xyz not found"


class TestConflictError:
    def test_default_values(self) -> None:
        err = ConflictError()
        assert err.status_code == 409

    def test_custom_detail(self) -> None:
        err = ConflictError("already exists")
        assert err.detail == "already exists"
