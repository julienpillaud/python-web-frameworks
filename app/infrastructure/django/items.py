from app.domain.entities import EntityId
from app.domain.items.entities import Item
from app.domain.items.repository import ItemRepositoryProtocol
from app.infrastructure.django.models.items import DjangoItemModel


class ItemRepository(ItemRepositoryProtocol):
    def get(self) -> list[Item]:
        orm_items = DjangoItemModel.objects.all()
        return [item.to_domain() for item in orm_items]

    def get_by_id(self, entity_id: EntityId) -> Item | None:
        orm_item = DjangoItemModel.objects.filter(id=entity_id).first()
        return orm_item.to_domain() if orm_item else None

    def save(self, entity: Item, /) -> None:
        DjangoItemModel.objects.create(
            id=entity.id,
            name=entity.name,
            description=entity.description,
        )

    def update(self, entity: Item, /) -> None:
        orm_item = DjangoItemModel.objects.get(id=entity.id)
        orm_item.name = entity.name
        orm_item.description = entity.description
        orm_item.save()

    def remove(self, entity: Item) -> None:
        DjangoItemModel.objects.filter(id=entity.id).delete()
