import json
from collections.abc import Callable
from typing import Any

from django.db import transaction
from django.http import HttpRequest, HttpResponse, JsonResponse
from pydantic import BaseModel, ValidationError

from app.api.django.types import EnhancedHttpRequest
from app.api.utils import ERROR_MAPPING
from app.domain.exceptions import DomainError

DJANGO_MIDDLEWARES = [
    "app.api.django.middlewares.DomainExceptionMiddleware",
    "app.api.django.middlewares.PydanticValidationMiddleware",
    "app.api.django.middlewares.TransactionMiddleware",
]


class BaseMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        return self.get_response(request)

    def get_json_body(self, request: HttpRequest) -> HttpResponse | dict[str, Any]:
        try:
            return json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse(
                content="Bad request",
                status=400,
                content_type="application/json",
            )


class DomainExceptionMiddleware(BaseMiddleware):
    def process_exception(
        self, request: HttpRequest, exc: Exception
    ) -> HttpResponse | None:
        if not isinstance(exc, DomainError):
            return None

        for error_cls in type(exc).mro():
            if issubclass(error_cls, DomainError) and error_cls in ERROR_MAPPING:
                return JsonResponse(
                    data={"detail": str(exc)},
                    status=ERROR_MAPPING[error_cls],
                )

        return HttpResponse(
            content="Internal Server Error",
            status=500,
            content_type="text/plain",
        )


class PydanticValidationMiddleware(BaseMiddleware):
    def process_view[T: BaseModel](
        self,
        request: EnhancedHttpRequest[T],
        view_func: Callable[[HttpRequest], HttpResponse],
        view_args: Any,
        view_kwargs: Any,
    ) -> HttpResponse | None:
        view_class = getattr(view_func, "view_class", None)
        if not view_class:
            return None

        body_models = getattr(view_class, "body_models", None)
        if not body_models:
            return None

        model = body_models.get(request.method)
        if not model:
            return None

        body = self.get_json_body(request)
        try:
            request.validated_data = model.model_validate(body)
            return None
        except ValidationError:
            return HttpResponse(
                content="Unprocessable content",
                status=422,
                content_type="application/json",
            )


class TransactionMiddleware(BaseMiddleware):
    def __call__(self, request: HttpRequest) -> HttpResponse:
        with transaction.atomic():
            return self.get_response(request)
