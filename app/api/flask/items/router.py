from typing import Any

from flask import Blueprint, Response, request

from app.api.flask.dependencies import get_context
from app.domain.entities import EntityId
from app.domain.items.commands import (
    create_item_command,
    delete_item_command,
    get_item_command,
    get_items_command,
    update_item_command,
)
from app.domain.items.entities import ItemCreate, ItemUpdate

router = Blueprint("items", __name__, url_prefix="/items")


@router.get("")
def get_items() -> Any:
    context = get_context()
    items = get_items_command(context)
    return [item.model_dump() for item in items]


@router.get("/<item_id>")
def get_item(item_id: EntityId) -> Response:
    context = get_context()
    item = get_item_command(context, item_id=item_id)
    return Response(
        response=item.model_dump_json(),
        status=200,
        content_type="application/json",
    )


@router.post("")
def create_item() -> Response:
    context = get_context()
    item_create = ItemCreate.model_validate(request.get_json())
    item = create_item_command(context, item_create=item_create)
    return Response(
        response=item.model_dump_json(),
        status=201,
        content_type="application/json",
    )


@router.patch("/<item_id>")
def update_item(item_id: EntityId) -> Response:
    context = get_context()
    item_update = ItemUpdate.model_validate(request.get_json())
    item = update_item_command(context, item_id=item_id, item_update=item_update)
    return Response(
        response=item.model_dump_json(),
        status=200,
        content_type="application/json",
    )


@router.delete("/<item_id>")
def delete_item(item_id: EntityId) -> Response:
    context = get_context()
    delete_item_command(context, item_id=item_id)
    return Response(
        status=204,
        content_type="application/json",
    )
