from typing import Any

from django.test import Client

from tests.api.clients.base import HTTPClient


class WrappedDjangoClient(HTTPClient):
    def __init__(self, client: Client) -> None:
        self._client = client

    def get(self, *args: Any, **kwargs: Any) -> Any:
        return self._client.get(*args, **kwargs)

    def post(self, *args: Any, **kwargs: Any) -> Any:
        if "json" in kwargs:
            kwargs["data"] = kwargs.pop("json")
            kwargs["content_type"] = "application/json"
        return self._client.post(*args, **kwargs)

    def patch(self, *args: Any, **kwargs: Any) -> Any:
        if "json" in kwargs:
            kwargs["data"] = kwargs.pop("json")
            kwargs["content_type"] = "application/json"
        return self._client.patch(*args, **kwargs)

    def delete(self, *args: Any, **kwargs: Any) -> Any:
        return self._client.delete(*args, **kwargs)
