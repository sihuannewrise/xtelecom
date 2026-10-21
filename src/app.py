from litestar import Litestar
from litestar.plugins.sqlalchemy import SQLAlchemyPlugin, SQLAlchemyAsyncConfig

from src.api.dependencies import dependencies
from src.api.routes import route_handlers
from src.infrastructure.config import get_engine, settings


def create_app() -> Litestar:
    db_config = SQLAlchemyAsyncConfig(
        engine_instance=get_engine(),
        before_send_handler="autocommit",
    )
    return Litestar(
        route_handlers=route_handlers,
        dependencies=dependencies,
        plugins=[SQLAlchemyPlugin(config=db_config)],
    )


app = create_app()
