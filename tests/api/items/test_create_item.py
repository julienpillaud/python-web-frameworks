import uuid

import pytest
from sqlalchemy.orm import Session
from starlette import status

from app.infrastructure.sqlalchemy.models.items import SQLItemModel
from tests.api.clients.base import HTTPClient
from tests.factories.items import ItemFactory


@pytest.mark.parametrize("client", ["fastapi", "flask", "django"], indirect=True)
def test_create_item(
    item_factory: ItemFactory,
    client: HTTPClient,
    session: Session,
) -> None:
    item = item_factory.build()
    data = item.model_dump(exclude={"id"})

    response = client.post("/items", json=data)

    assert response.status_code == status.HTTP_201_CREATED
    result = response.json()
    assert "id" in result
    assert result["name"] == item.name
    assert result["description"] == item.description

    item_id = uuid.UUID(result["id"])
    item_db = session.get(SQLItemModel, item_id)
    assert item_db
    assert item_db.id == item_id
    assert item_db.name == item.name
    assert item_db.description == item.description


@pytest.mark.parametrize("client", ["fastapi", "flask", "django"], indirect=True)
def test_create_item_invalid_data(client: HTTPClient) -> None:
    response = client.post("/items", json={"data": "invalid"})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
