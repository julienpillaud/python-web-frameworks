from typing import Any

from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from tests.api.clients.base import HTTPClient


class WrappedFlaskResponse:
    def __init__(self, response: TestResponse) -> None:
        self._response = response

    @property
    def status_code(self) -> int:
        return self._response.status_code

    def json(self) -> Any:
        return self._response.json

    @property
    def text(self) -> Any:
        return self._response.text


class WrappedFlaskClient(HTTPClient):
    def __init__(self, client: FlaskClient) -> None:
        self._client = client

    def get(self, *args: Any, **kwargs: Any) -> Any:
        response = self._client.get(*args, **kwargs)
        return WrappedFlaskResponse(response=response)

    def post(self, *args: Any, **kwargs: Any) -> Any:
        if "params" in kwargs:
            kwargs["query_string"] = kwargs.pop("params")
        response = self._client.post(*args, **kwargs)
        return WrappedFlaskResponse(response=response)

    def patch(self, *args: Any, **kwargs: Any) -> Any:
        response = self._client.patch(*args, **kwargs)
        return WrappedFlaskResponse(response=response)

    def delete(self, *args: Any, **kwargs: Any) -> Any:
        response = self._client.delete(*args, **kwargs)
        return WrappedFlaskResponse(response=response)
