from functools import cached_property

from sqlalchemy.orm import Session

from app.core.settings import AppEnvironment, Settings
from app.domain.context import ContextProtocol
from app.domain.items.repository import ItemRepositoryProtocol
from app.infrastructure.sqlalchemy.items import SQLItemRepository


class Context(ContextProtocol):
    def __init__(self, settings: Settings, sql_session: Session) -> None:
        self.settings = settings
        self.sql_session = sql_session

    @property
    def environment(self) -> AppEnvironment:
        # property to test dependencies override
        return self.settings.environment

    @cached_property
    def item_repository(self) -> ItemRepositoryProtocol:
        return SQLItemRepository(session=self.sql_session)
