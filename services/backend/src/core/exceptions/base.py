class AppError(Exception):
    status_code: int = 500
    detail: str = "Internal server error"

    def __init__(
        self,
        detail: str | None = None,
        status_code: int | None = None,
    ) -> None:
        self.detail = detail or self.__class__.detail
        self.status_code = status_code or self.__class__.status_code
        super().__init__(self.detail)
