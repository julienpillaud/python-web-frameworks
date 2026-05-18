from pydantic import BaseModel

from app.domain.entities import DomainEntity


class Item(DomainEntity):
    name: str
    description: str


class ItemCreate(BaseModel):
    name: str
    description: str


class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
