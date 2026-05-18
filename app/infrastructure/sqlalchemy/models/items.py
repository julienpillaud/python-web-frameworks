from sqlalchemy.orm import Mapped

from app.domain.items.entities import Item
from app.infrastructure.sqlalchemy.models.base import OrmEntity


class SQLItemModel(OrmEntity):
    __tablename__ = "items"

    name: Mapped[str]
    description: Mapped[str]

    @classmethod
    def from_domain(cls, item: Item, /) -> SQLItemModel:
        return cls(
            id=item.id,
            name=item.name,
            description=item.description,
        )

    def to_domain(self) -> Item:
        return Item(
            id=self.id,
            name=self.name,
            description=self.description,
        )
