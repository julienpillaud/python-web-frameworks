from typing import Literal

from pydantic import BaseModel

from app.domain.context import ContextProtocol
from app.domain.entities import EntityId
from app.domain.exceptions import BadRequestError
from app.domain.items.entities import Item


class UnexpectedError(Exception):
    pass


class ItemCreateError(BaseModel):
    id: EntityId


def create_item_error_command(
    context: ContextProtocol,
    /,
    item_create: ItemCreateError,
    error_type: Literal["domain", "unexpected"] | None = None,
) -> Item:
    item = Item(id=item_create.id, name="Item", description="Wonderful item")
    context.item_repository.save(item)

    if error_type == "domain":
        raise BadRequestError("Bad Request")

    if error_type == "unexpected":
        raise UnexpectedError()

    return item
