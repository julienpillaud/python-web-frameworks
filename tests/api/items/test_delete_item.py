import uuid

import pytest
from sqlalchemy.orm import Session
from starlette import status

from app.infrastructure.sqlalchemy.models.items import SQLItemModel
from tests.api.clients.base import HTTPClient
from tests.factories.items import ItemFactory


@pytest.mark.parametrize("client", ["fastapi", "flask", "django"], indirect=True)
def test_delete_item(
    item_factory: ItemFactory,
    client: HTTPClient,
    session: Session,
) -> None:
    item = item_factory.create_one()

    response = client.delete(f"/items/{item.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    item_db = session.get(SQLItemModel, item.id)
    assert item_db is None


@pytest.mark.parametrize("client", ["fastapi", "flask", "django"], indirect=True)
def test_delete_item_not_found(client: HTTPClient) -> None:
    response = client.delete(f"/items/{uuid.uuid7()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
