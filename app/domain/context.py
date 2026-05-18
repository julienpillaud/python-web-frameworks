from typing import Protocol

from app.domain.items.repository import ItemRepositoryProtocol


class ContextProtocol(Protocol):
    @property
    def item_repository(self) -> ItemRepositoryProtocol: ...
