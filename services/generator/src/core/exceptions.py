class AppError(Exception):
    detail: str = "Internal error"

    def __init__(self, detail: str | None = None) -> None:
        self.detail = detail or self.__class__.detail
        super().__init__(self.detail)


class PoolExhaustedError(AppError):
    detail = "Slug pool is exhausted"
