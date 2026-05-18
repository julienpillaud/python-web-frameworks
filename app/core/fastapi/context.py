from functools import cached_property

from sqlalchemy.orm import Session

from app.domain.context import ContextProtocol
from app.domain.items.repository import ItemRepositoryProtocol
from app.infrastructure.sqlalchemy.items import SQLItemRepository


class Context(ContextProtocol):
    def __init__(self, sql_session: Session) -> None:
        self.sql_session = sql_session

    @cached_property
    def item_repository(self) -> ItemRepositoryProtocol:
        return SQLItemRepository(session=self.sql_session)
