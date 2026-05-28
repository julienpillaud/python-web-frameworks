import pytest
from starlette import status

from tests.api.clients.base import HTTPClient
from tests.factories.items import ItemFactory


@pytest.mark.parametrize("client", ["fastapi", "flask", "django"], indirect=True)
def test_get_items(item_factory: ItemFactory, client: HTTPClient) -> None:
    items_count = 3
    item_factory.create_many(items_count)

    response = client.get("/items")

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result) == items_count
