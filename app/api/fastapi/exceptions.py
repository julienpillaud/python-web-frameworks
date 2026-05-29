from fastapi import FastAPI, status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.api.utils import ERROR_MAPPING
from app.domain.exceptions import (
    DomainError,
)


def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal Server Error"},
        )

    @app.exception_handler(DomainError)
    async def domain_exception_handler(
        request: Request,
        exc: DomainError,
    ) -> JSONResponse:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        for error_cls in type(exc).mro():
            if issubclass(error_cls, DomainError) and error_cls in ERROR_MAPPING:
                status_code = ERROR_MAPPING[error_cls]
                break

        return JSONResponse(status_code=status_code, content={"detail": str(exc)})
