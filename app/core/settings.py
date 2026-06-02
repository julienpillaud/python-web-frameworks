from enum import StrEnum
from typing import Any

from pydantic import BaseModel, PostgresDsn, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.api.django.middlewares import DJANGO_MIDDLEWARES
from app.infrastructure.django.apps import DJANGO_APPS


class AppEnvironment(StrEnum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class DjangoSettings(BaseModel):
    debug: bool = False
    secret_key: str
    root_urlconf: str = "app.api.django.urls"
    installed_apps: list[str] = DJANGO_APPS
    middleware: list[str] = DJANGO_MIDDLEWARES


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        frozen=True,
        env_file=".env",
        env_nested_delimiter="__",
        nested_model_default_partial_update=True,
    )

    environment: AppEnvironment

    django: DjangoSettings

    postgres_user: str
    postgres_password: SecretStr
    postgres_host: str
    postgres_port: int = 5432
    postgres_db: str
    postgres_params: dict[str, Any] = {}

    @computed_field
    @property
    def postgres_dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.postgres_user,
            password=self.postgres_password.get_secret_value(),
            host=self.postgres_host,
            port=self.postgres_port,
            path=self.postgres_db,
        )

    @computed_field
    @property
    def django_postgres(self) -> dict[str, Any]:
        return {
            "ENGINE": "django.db.backends.postgresql",
            "USER": self.postgres_user,
            "PASSWORD": self.postgres_password.get_secret_value(),
            "HOST": self.postgres_host,
            "PORT": self.postgres_port,
            "NAME": self.postgres_db,
        }
