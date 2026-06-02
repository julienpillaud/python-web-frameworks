from collections.abc import AsyncIterator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI

from app.api.logger import logger
from app.core.settings import Settings
from app.infrastructure.sqlalchemy.utils import SQLResource


def lifespan_factory(
    settings: Settings,
) -> Callable[[FastAPI], AbstractAsyncContextManager[None]]:

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        sql_resource = SQLResource.from_settings(settings)
        app.state.sql_resource = sql_resource
        logger.info("Application startup complete")

        yield

        sql_resource.release()
        logger.info("Application shutdown complete")

    return lifespan
