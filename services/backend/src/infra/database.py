from litestar.plugins.sqlalchemy import (
    SQLAlchemyPlugin,
    SQLAlchemyAsyncConfig,
    EngineConfig,
    AsyncSessionConfig,
)
from src.core.config import PostgresConfig


def get_db_plugin(config: PostgresConfig) -> SQLAlchemyPlugin:
    return SQLAlchemyPlugin(
            SQLAlchemyAsyncConfig(
                engine_config=EngineConfig(
                    echo=config.echo,
                    echo_pool=config.echo_pool,
                    pool_size=config.pool_size,
                    max_overflow=config.max_overflow,
                    pool_pre_ping=config.pool_pre_ping,
                    pool_timeout=config.pool_timeout,
                ),
                session_config=AsyncSessionConfig(
                    autoflush=False,
                    expire_on_commit=False,
                ),
                connection_string=str(config.url),
            ),
        )
