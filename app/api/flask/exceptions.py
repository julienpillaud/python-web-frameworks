from flask import Flask, Response
from pydantic import ValidationError

from app.api.utils import ERROR_MAPPING
from app.domain.exceptions import DomainError


def add_exception_handlers(app: Flask) -> None:
    @app.errorhandler(DomainError)
    def domain_exception_handler(exc: DomainError) -> Response:
        for error_cls in type(exc).mro():
            if issubclass(error_cls, DomainError) and error_cls in ERROR_MAPPING:
                return Response(
                    response="{'detail': str(exc)}",
                    status=ERROR_MAPPING[error_cls],
                )

        return Response(
            response="Internal Server Error",
            status=500,
            content_type="text/plain",
        )

    @app.errorhandler(ValidationError)
    def pydantic_validation_exception_handler(exc: ValidationError) -> Response:
        return Response(
            response=exc.json(),
            status=422,
            content_type="application/json",
        )
