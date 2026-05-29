from collections.abc import Iterator

import django
import pytest
from django.conf import settings
from django.test import Client
from fastapi import FastAPI
from fastapi.testclient import TestClient
from flask import Flask

from app.api.fastapi.app import create_fastapi_app
from app.api.fastapi.dependencies import get_settings
from app.api.flask.app import create_flask_app
from app.core.settings import Settings
from tests.api.clients.base import HTTPClient
from tests.api.clients.django import WrappedDjangoClient
from tests.api.clients.flask import WrappedFlaskClient
from tests.conftest import settings_override_func


@pytest.fixture(scope="session")
def fastapi_app(app_settings: Settings) -> FastAPI:
    app = create_fastapi_app(settings=app_settings)
    app.dependency_overrides[get_settings] = settings_override_func
    return app


@pytest.fixture(scope="session")
def flask_app(app_settings: Settings) -> Flask:
    app = create_flask_app(settings=app_settings)
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
    flask_app: Flask,
    django_setup: None,
) -> Iterator[HTTPClient]:
    if request.param == "fastapi":
        with TestClient(fastapi_app, raise_server_exceptions=False) as client:
            yield client
    elif request.param == "flask":
        yield WrappedFlaskClient(flask_app.test_client())
    elif request.param == "django":
        yield WrappedDjangoClient(Client())
