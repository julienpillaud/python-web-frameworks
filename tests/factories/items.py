import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.domain.items.entities import Item
from app.infrastructure.sqlalchemy.models.items import SQLItemModel
from tests.factories.utils import faker


def generate_item(**kwargs: Any) -> Item:
    return Item(
        id=uuid.uuid7(),
        name=kwargs.get("name", faker.random_string()),
        description=kwargs.get("description", faker.random_string()),
    )


class ItemFactory:
    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def build(**kwargs: Any) -> Item:
        return generate_item(**kwargs)

    def create_one(self, **kwargs: Any) -> Item:
        item = self.build(**kwargs)
        self._save([item])
        return item

    def create_many(self, count: int, /, **kwargs: Any) -> list[Item]:
        items = [self.build(**kwargs) for _ in range(count)]
        self._save(items)
        return items

    def _save(self, items: list[Item]) -> None:
        orm_items = [SQLItemModel.from_domain(item) for item in items]
        self.session.bulk_save_objects(orm_items)
        self.session.commit()
