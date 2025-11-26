import logging
from typing import Literal
from pathlib import Path

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent.parent


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


class PostgresConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10
    pool_pre_ping: bool = True
    pool_timeout: int = 30


class AppConfig(BaseModel):
    debug: bool = False
    generate_openapi: bool = False


class Settings(BaseSettings):
    app: AppConfig
    database: PostgresConfig

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


settings = Settings()  # type: ignore
