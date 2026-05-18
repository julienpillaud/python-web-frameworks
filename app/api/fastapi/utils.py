from collections.abc import AsyncIterator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.logger import logger
from app.core.settings import Settings


def lifespan_factory(
    settings: Settings,
) -> Callable[[FastAPI], AbstractAsyncContextManager[None]]:

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        engine = create_engine(
            url=str(settings.postgres_dsn),
            **settings.postgres_params,
        )
        app.state.sql_engine = engine
        app.state.sql_session_factory = sessionmaker(bind=engine)
        logger.info("Application startup complete")

        yield

        engine.dispose()
        logger.info("Application shutdown complete")

    return lifespan
