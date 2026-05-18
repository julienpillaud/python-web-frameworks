from functools import cached_property

from app.domain.context import ContextProtocol
from app.domain.items.repository import ItemRepositoryProtocol
from app.infrastructure.django.items import ItemRepository


class Context(ContextProtocol):
    @cached_property
    def item_repository(self) -> ItemRepositoryProtocol:
        return ItemRepository()
