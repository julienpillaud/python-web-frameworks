from collections.abc import Iterator
from typing import Any, Protocol

import django
import pytest
from django.conf import settings
from django.test import Client
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.fastapi.app import create_fastapi_app
from app.api.fastapi.dependencies import get_settings
from app.core.settings import Settings
from tests.conftest import settings_override_func


class HTTPClient(Protocol):
    def get(self, *args: Any, **kwargs: Any) -> Any: ...
    def post(self, *args: Any, **kwargs: Any) -> Any: ...
    def patch(self, *args: Any, **kwargs: Any) -> Any: ...
    def delete(self, *args: Any, **kwargs: Any) -> Any: ...


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


@pytest.fixture(scope="session")
def fastapi_app(app_settings: Settings) -> FastAPI:
    app = create_fastapi_app(settings=app_settings)
    app.dependency_overrides[get_settings] = settings_override_func
    return app


@pytest.fixture(scope="session")
def django_setup(app_settings: Settings) -> None:
    settings.configure(
        DEBUG=app_settings.django.debug,
        SECRET_KEY=app_settings.django.secret_key,
        ROOT_URLCONF=app_settings.django.root_urlconf,
        INSTALLED_APPS=app_settings.django.installed_apps,
        MIDDLEWARE=app_settings.django.middleware,
        DATABASES={"default": app_settings.django_postgres},
        ALLOWED_HOSTS=["testserver"],
    )
    django.setup()


@pytest.fixture
def client(
    request: pytest.FixtureRequest,
    fastapi_app: FastAPI,
    django_setup: None,
) -> Iterator[HTTPClient]:
    if request.param == "fastapi":
        with TestClient(fastapi_app) as client:
            yield client
    elif request.param == "django":
        yield WrappedDjangoClient(Client())
