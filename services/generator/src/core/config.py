import logging
from typing import Literal
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class LoggingConfig(BaseModel):
    level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    format: str = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"

    @property
    def level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.level.upper()]


class AppConfig(BaseModel):
    debug: bool = False


class NatsConfig(BaseModel):
    url: str


class Settings(BaseSettings):
    app: AppConfig
    broker: NatsConfig
    logging: LoggingConfig

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


settings = Settings()  # type: ignore
