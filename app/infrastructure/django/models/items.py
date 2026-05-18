from django.db import models

from app.domain.items.entities import Item


class DjangoItemModel(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField()
    description = models.CharField()

    class Meta:
        db_table = "items"

    def to_domain(self) -> Item:
        return Item(
            id=self.id,
            name=self.name,
            description=self.description,
        )
