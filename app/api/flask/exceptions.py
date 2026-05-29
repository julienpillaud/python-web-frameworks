import json

from flask import Flask, Response, g
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

from app.api.utils import ERROR_MAPPING
from app.domain.exceptions import DomainError


def add_exception_handlers(app: Flask) -> None:
    @app.errorhandler(Exception)
    def exception_handler(exc: Exception) -> Response:
        # Ensure rollback in teardown
        g.error = True
        g.exception = exc

        return Response(
            response=json.dumps({"detail": "Internal Server Error"}),
            status=500,
            content_type="application/json",
        )

    @app.errorhandler(HTTPException)
    def http_exception_handler(exc: HTTPException) -> Response:
        # Ensure rollback in teardown
        g.error = True
        g.exception = exc

        return Response(
            response=json.dumps({"detail": exc.description}),
            status=exc.code,
            content_type="application/json",
        )

    @app.errorhandler(DomainError)
    def domain_exception_handler(exc: DomainError) -> Response:
        # Ensure rollback in teardown
        g.error = True
        g.exception = exc

        status_code = 500

        for error_cls in type(exc).mro():
            if issubclass(error_cls, DomainError) and error_cls in ERROR_MAPPING:
                status_code = ERROR_MAPPING[error_cls]
                break

        return Response(
            response=json.dumps({"detail": str(exc)}),
            status=status_code,
            content_type="application/json",
        )

    @app.errorhandler(ValidationError)
    def pydantic_validation_exception_handler(exc: ValidationError) -> Response:
        return Response(
            response=exc.json(),
            status=422,
            content_type="application/json",
        )
