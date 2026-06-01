import uuid
from typing import Annotated, ClassVar

from django.http import HttpRequest, JsonResponse
from django.views import View
from fast_depends import Depends, inject
from pydantic import BaseModel

from app.api.django.dependencies import get_context
from app.api.django.types import EnhancedHttpRequest
from app.core.django.context import Context
from app.domain.dev.commands import ItemCreateError, create_item_error_command
from app.domain.items.commands import (
    create_item_command,
    delete_item_command,
    get_item_command,
    get_items_command,
    update_item_command,
)
from app.domain.items.entities import ItemCreate, ItemUpdate


class ItemView(View):
    body_models: ClassVar[dict[str, type[BaseModel]]] = {"POST": ItemCreate}

    @inject
    def get(
        self,
        request: HttpRequest,
        context: Annotated[Context, Depends(get_context)],
    ) -> JsonResponse:
        items = get_items_command(context)
        return JsonResponse(data=[item.model_dump() for item in items], safe=False)

    @inject(cast=False)
    def post(
        self,
        request: EnhancedHttpRequest[ItemCreate],
        context: Annotated[Context, Depends(get_context)],
    ) -> JsonResponse:
        item = create_item_command(context, item_create=request.validated_data)
        return JsonResponse(item.model_dump(), status=201, safe=False)


class ItemViewDetail(View):
    body_models: ClassVar[dict[str, type[BaseModel]]] = {"PATCH": ItemUpdate}

    @inject
    def get(
        self,
        request: HttpRequest,
        item_id: uuid.UUID,
        context: Annotated[Context, Depends(get_context)],
    ) -> JsonResponse:
        item = get_item_command(context, item_id=item_id)
        return JsonResponse(data=item.model_dump(), safe=False)

    @inject(cast=False)
    def patch(
        self,
        request: EnhancedHttpRequest[ItemUpdate],
        item_id: uuid.UUID,
        context: Annotated[Context, Depends(get_context)],
    ) -> JsonResponse:
        item = update_item_command(
            context,
            item_id=item_id,
            item_update=request.validated_data,
        )
        return JsonResponse(data=item.model_dump(), safe=False)

    @inject
    def delete(
        self,
        request: HttpRequest,
        item_id: uuid.UUID,
        context: Annotated[Context, Depends(get_context)],
    ) -> JsonResponse:
        delete_item_command(context, item_id=item_id)
        return JsonResponse(data="", status=204, safe=False)


class ItemViewSpecial(View):
    body_models: ClassVar[dict[str, type[BaseModel]]] = {"POST": ItemCreateError}

    @inject(cast=False)
    def post(
        self,
        request: EnhancedHttpRequest[ItemCreateError],
        context: Annotated[Context, Depends(get_context)],
    ) -> JsonResponse:
        error_type = request.GET.get("error_type")
        item = create_item_error_command(
            context,
            item_create=request.validated_data,
            error_type=error_type,  # ty:ignore[invalid-argument-type]
        )
        return JsonResponse(data=item.model_dump(), safe=False)
