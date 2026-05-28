from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from app.api.fastapi.dependencies import get_context
from app.core.sqlalchemy.context import Context
from app.domain.entities import EntityId
from app.domain.items.commands import (
    create_item_command,
    delete_item_command,
    get_item_command,
    get_items_command,
    update_item_command,
)
from app.domain.items.entities import Item, ItemCreate, ItemUpdate

router = APIRouter(prefix="/items")


@router.get("", response_model=list[Item])
def get_items(
    context: Annotated[Context, Depends(get_context)],
) -> Any:
    return get_items_command(context)


@router.get("/{item_id}", response_model=Item)
def get_item(
    item_id: EntityId,
    context: Annotated[Context, Depends(get_context)],
) -> Any:
    return get_item_command(context, item_id=item_id)


@router.post("", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(
    item_create: ItemCreate,
    context: Annotated[Context, Depends(get_context)],
) -> Any:
    return create_item_command(context, item_create=item_create)


@router.patch("/{item_id}", response_model=Item)
def update_item(
    item_id: EntityId,
    item_update: ItemUpdate,
    context: Annotated[Context, Depends(get_context)],
) -> Any:
    return update_item_command(context, item_id=item_id, item_update=item_update)


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_item(
    item_id: EntityId,
    context: Annotated[Context, Depends(get_context)],
) -> None:
    delete_item_command(context, item_id=item_id)
