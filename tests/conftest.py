from functools import lru_cache

import pytest
from pydantic import SecretStr

from app.core.settings import DjangoSettings, Settings

pytest_plugins = [
    "tests.plugins.database",
    "tests.plugins.factories",
]


@lru_cache
def settings_override_func() -> Settings:
    return Settings(
        postgres_user="user",
        postgres_password=SecretStr("password"),
        postgres_host="localhost",
        postgres_db="test",
        django=DjangoSettings(secret_key="secret"),
        postgres_params={"echo": True},
    )


@pytest.fixture(scope="session")
def app_settings() -> Settings:
    return settings_override_func()
