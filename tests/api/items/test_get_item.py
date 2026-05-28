import uuid

import pytest
from starlette import status

from tests.api.clients.base import HTTPClient
from tests.factories.items import ItemFactory


@pytest.mark.parametrize("client", ["fastapi", "flask", "django"], indirect=True)
def test_get_item(item_factory: ItemFactory, client: HTTPClient) -> None:
    item = item_factory.create_one()

    response = client.get(f"/items/{item.id}")

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["id"] == str(item.id)
    assert result["name"] == item.name
    assert result["description"] == item.description


@pytest.mark.parametrize("client", ["fastapi", "flask", "django"], indirect=True)
def test_get_item_not_found(client: HTTPClient) -> None:
    item_id = uuid.uuid7()

    response = client.get(f"/items/{item_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
