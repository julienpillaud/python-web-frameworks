from fastapi import FastAPI, status
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse, Response

from app.api.utils import ERROR_MAPPING
from app.domain.exceptions import (
    DomainError,
)


def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def domain_exception_handler(request: Request, exc: DomainError) -> Response:
        for error_cls in type(exc).mro():
            if issubclass(error_cls, DomainError) and error_cls in ERROR_MAPPING:
                return JSONResponse(
                    status_code=ERROR_MAPPING[error_cls],
                    content={"detail": str(exc)},
                )

        return PlainTextResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Internal Server Error",
        )
