from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session

from app.domain.entities import EntityId
from app.domain.items.entities import Item
from app.domain.items.repository import ItemRepositoryProtocol
from app.infrastructure.sqlalchemy.models.items import SQLItemModel


class SQLItemRepository(ItemRepositoryProtocol):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self) -> list[Item]:
        stmt = select(SQLItemModel)
        orm_items = self.session.scalars(stmt).all()
        return [orm_item.to_domain() for orm_item in orm_items]

    def get_by_id(self, entity_id: EntityId) -> Item | None:
        stmt = select(SQLItemModel).where(SQLItemModel.id == entity_id)
        orm_item = self.session.scalars(stmt).one_or_none()
        return orm_item.to_domain() if orm_item else None

    def save(self, entity: Item, /) -> None:
        stmt = insert(SQLItemModel).values(
            id=entity.id,
            name=entity.name,
            description=entity.description,
        )
        self.session.execute(stmt)

    def update(self, entity: Item, /) -> None:
        stmt = (
            update(SQLItemModel)
            .where(SQLItemModel.id == entity.id)
            .values(
                name=entity.name,
                description=entity.description,
            )
        )
        self.session.execute(stmt)

    def remove(self, entity: Item) -> None:
        stmt = delete(SQLItemModel).where(SQLItemModel.id == entity.id)
        self.session.execute(stmt)
