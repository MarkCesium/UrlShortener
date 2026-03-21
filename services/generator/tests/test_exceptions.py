from src.core.exceptions import AppError, PoolExhaustedError


class TestAppError:
    def test_default_detail(self) -> None:
        err = AppError()
        assert err.detail == "Internal error"
        assert str(err) == "Internal error"

    def test_custom_detail(self) -> None:
        err = AppError("something broke")
        assert err.detail == "something broke"


class TestPoolExhaustedError:
    def test_is_app_error(self) -> None:
        err = PoolExhaustedError()
        assert isinstance(err, AppError)

    def test_default_detail(self) -> None:
        err = PoolExhaustedError()
        assert err.detail == "Slug pool is exhausted"
