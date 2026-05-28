import uuid

import pytest
from starlette import status

from tests.api.clients.base import HTTPClient
from tests.factories.items import ItemFactory


@pytest.mark.parametrize("client", ["fastapi", "flask", "django"], indirect=True)
def test_delete_item(item_factory: ItemFactory, client: HTTPClient) -> None:
    item = item_factory.create_one()

    response = client.delete(f"/items/{item.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.parametrize("client", ["fastapi", "flask", "django"], indirect=True)
def test_delete_item_not_found(client: HTTPClient) -> None:
    response = client.delete(f"/items/{uuid.uuid7()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
