import uuid

import pytest
from starlette import status

from tests.api.conftest import HTTPClient
from tests.factories.items import ItemFactory


@pytest.mark.parametrize("client", ["fastapi", "django"], indirect=True)
def test_update_item(item_factory: ItemFactory, client: HTTPClient) -> None:
    updated_name = "New name"
    updated_description = "New description"
    data = {"name": updated_name, "description": updated_description}
    item = item_factory.create_one()

    response = client.patch(f"/items/{item.id}", json=data)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["id"] == str(item.id)
    assert result["name"] == updated_name
    assert result["description"] == updated_description


@pytest.mark.parametrize("client", ["fastapi", "django"], indirect=True)
def test_update_item_name(item_factory: ItemFactory, client: HTTPClient) -> None:
    updated_name = "New name"
    data = {"name": updated_name}
    item = item_factory.create_one()

    response = client.patch(f"/items/{item.id}", json=data)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["id"] == str(item.id)
    assert result["name"] == updated_name
    assert result["description"] == item.description


@pytest.mark.parametrize("client", ["fastapi", "django"], indirect=True)
def test_update_item_description(item_factory: ItemFactory, client: HTTPClient) -> None:
    updated_description = "New description"
    data = {"description": updated_description}
    item = item_factory.create_one()

    response = client.patch(f"/items/{item.id}", json=data)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["id"] == str(item.id)
    assert result["name"] == item.name
    assert result["description"] == updated_description


@pytest.mark.parametrize("client", ["fastapi", "django"], indirect=True)
def test_get_item_not_found(client: HTTPClient) -> None:
    updated_name = "Updated"

    response = client.patch(f"/items/{uuid.uuid7()}", json={"name": updated_name})

    assert response.status_code == status.HTTP_404_NOT_FOUND
