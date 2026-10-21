import ssl
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        extra="ignore",
    )

    database_url: str = "postgresql+asyncpg://knhdb1:knhdb1@db.knh.cloud:443/knhdb1"

    db_ssl_enabled: bool = True
    db_ssl_check_hostname: bool = False
    db_ssl_verify: bool = False

    db_echo: bool = True

    debug: bool = False
    xml_upload_dir: str = "uploads"


settings = Settings()


def _build_ssl_context() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    ctx.check_hostname = settings.db_ssl_check_hostname
    ctx.verify_mode = (
        ssl.CERT_NONE if not settings.db_ssl_verify else ssl.CERT_REQUIRED
    )
    return ctx


def build_connect_args() -> dict:
    """connect_args для asyncpg — те же, что в вашем рабочем подключении."""
    if not settings.db_ssl_enabled:
        return {}
    return {
        "ssl": _build_ssl_context(),
        "direct_tls": True,
    }


@lru_cache(maxsize=1)
def get_engine() -> AsyncEngine:
    """
    Единая точка создания engine.
    Используется в Litestar-плагине и в Alembic, чтобы не дублировать SSL-настройки.
    """
    return create_async_engine(
        settings.database_url,
        echo=settings.db_echo,
        connect_args=build_connect_args(),
    )
