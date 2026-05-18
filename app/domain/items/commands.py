import uuid

from app.domain.context import ContextProtocol
from app.domain.entities import EntityId
from app.domain.exceptions import NotFoundError
from app.domain.items.entities import Item, ItemCreate, ItemUpdate


def get_items_command(context: ContextProtocol, /) -> list[Item]:
    return context.item_repository.get()


def get_item_command(context: ContextProtocol, /, item_id: EntityId) -> Item:
    item = context.item_repository.get_by_id(item_id)
    if not item:
        raise NotFoundError("Item not found")

    return item


def create_item_command(
    context: ContextProtocol,
    /,
    item_create: ItemCreate,
) -> Item:
    item = Item(
        id=uuid.uuid7(),
        name=item_create.name,
        description=item_create.description,
    )
    context.item_repository.save(item)
    return item


def update_item_command(
    context: ContextProtocol,
    /,
    item_id: EntityId,
    item_update: ItemUpdate,
) -> Item:
    item = context.item_repository.get_by_id(item_id)
    if not item:
        raise NotFoundError("Item not found")

    if item_update.name is not None:
        item.name = item_update.name
    if item_update.description is not None:
        item.description = item_update.description

    context.item_repository.update(item)
    return item


def delete_item_command(context: ContextProtocol, /, item_id: EntityId) -> None:
    item = context.item_repository.get_by_id(item_id)
    if not item:
        raise NotFoundError("Item not found")

    context.item_repository.remove(item)
