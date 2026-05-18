from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.domain.entities import EntityId


class OrmEntity(DeclarativeBase):
    id: Mapped[EntityId] = mapped_column(primary_key=True)
