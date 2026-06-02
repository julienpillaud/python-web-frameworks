from functools import cached_property

from app.core.settings import AppEnvironment, Settings
from app.domain.context import ContextProtocol
from app.domain.items.repository import ItemRepositoryProtocol
from app.infrastructure.django.items import ItemRepository


class Context(ContextProtocol):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @property
    def environment(self) -> AppEnvironment:
        # property to test dependencies override
        return self.settings.environment

    @cached_property
    def item_repository(self) -> ItemRepositoryProtocol:
        return ItemRepository()
