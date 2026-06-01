import uuid

import pytest
from fastapi import status
from sqlalchemy.orm import Session

from app.infrastructure.sqlalchemy.models.items import SQLItemModel
from tests.api.clients.base import HTTPClient


@pytest.mark.parametrize("client", ["fastapi", "flask", "django"], indirect=True)
def test_item_domain_error(client: HTTPClient, session: Session) -> None:
    item_id = uuid.uuid7()

    response = client.post(
        "/dev/error",
        params={"error_type": "domain"},
        json={"id": str(item_id)},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    result = response.json()
    assert result["detail"] == "Bad Request"

    # Check rollback after error
    item_db = session.get(SQLItemModel, item_id)
    assert item_db is None


@pytest.mark.parametrize("client", ["fastapi", "flask", "django"], indirect=True)
def test_item_unexpected_error(client: HTTPClient, session: Session) -> None:
    item_id = uuid.uuid7()

    response = client.post(
        "/dev/error",
        params={"error_type": "unexpected"},
        json={"id": str(item_id)},
    )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.text == "Internal Server Error"

    # Check rollback after error
    item_db = session.get(SQLItemModel, item_id)
    assert item_db is None


@pytest.mark.parametrize("client", ["fastapi", "flask", "django"], indirect=True)
def test_http_error(client: HTTPClient) -> None:
    response = client.get("/unknown")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    result = response.json()
    assert "not found" in result["detail"].lower()
