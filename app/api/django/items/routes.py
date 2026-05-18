import uuid
from typing import ClassVar

from django.http import HttpRequest, JsonResponse
from django.views import View
from pydantic import BaseModel

from app.api.django.types import EnhancedHttpRequest
from app.core.django.context import Context
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

    def get(self, request: HttpRequest) -> JsonResponse:
        context = Context()
        items = get_items_command(context)
        return JsonResponse(data=[item.model_dump() for item in items], safe=False)

    def post(self, request: EnhancedHttpRequest[ItemCreate]) -> JsonResponse:
        context = Context()
        item = create_item_command(context, item_create=request.validated_data)
        return JsonResponse(item.model_dump(), status=201, safe=False)


class ItemViewDetail(View):
    body_models: ClassVar[dict[str, type[BaseModel]]] = {"PATCH": ItemUpdate}

    def get(self, request: HttpRequest, item_id: uuid.UUID) -> JsonResponse:
        context = Context()
        item = get_item_command(context, item_id=item_id)
        return JsonResponse(data=item.model_dump(), safe=False)

    def patch(
        self,
        request: EnhancedHttpRequest[ItemUpdate],
        item_id: uuid.UUID,
    ) -> JsonResponse:
        context = Context()
        item = update_item_command(
            context,
            item_id=item_id,
            item_update=request.validated_data,
        )
        return JsonResponse(data=item.model_dump(), safe=False)

    def delete(self, request: HttpRequest, item_id: uuid.UUID) -> JsonResponse:
        context = Context()
        delete_item_command(context, item_id=item_id)
        return JsonResponse(data="", status=204, safe=False)
