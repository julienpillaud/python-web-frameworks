from fastapi import FastAPI

from app.api.fastapi.exceptions import add_exception_handlers
from app.api.fastapi.items.router import router as items_router
from app.api.fastapi.lifespan import lifespan_factory
from app.core.settings import Settings


def create_fastapi_app(settings: Settings) -> FastAPI:
    app = FastAPI(lifespan=lifespan_factory(settings=settings))

    add_exception_handlers(app=app)
    app.include_router(items_router)

    return app
