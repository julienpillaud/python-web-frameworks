from typing import Any

from flask.testing import FlaskClient

from tests.api.clients.base import HTTPClient


class WrappedFlaskResponse:
    def __init__(self, response: Any) -> None:
        self._response = response

    @property
    def status_code(self) -> int:
        return self._response.status_code

    def json(self) -> Any:
        return self._response.json


class WrappedFlaskClient(HTTPClient):
    def __init__(self, client: FlaskClient) -> None:
        self._client = client

    def get(self, *args: Any, **kwargs: Any) -> Any:
        return WrappedFlaskResponse(self._client.get(*args, **kwargs))

    def post(self, *args: Any, **kwargs: Any) -> Any:
        return WrappedFlaskResponse(self._client.post(*args, **kwargs))

    def patch(self, *args: Any, **kwargs: Any) -> Any:
        return WrappedFlaskResponse(self._client.patch(*args, **kwargs))

    def delete(self, *args: Any, **kwargs: Any) -> Any:
        return WrappedFlaskResponse(self._client.delete(*args, **kwargs))
