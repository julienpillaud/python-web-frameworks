from flask import Flask

from app.core.settings import Settings
from app.infrastructure.sqlalchemy.utils import SQLResource


def init_app(settings: Settings, app: Flask) -> None:
    sql_resource = SQLResource.from_settings(settings)
    app.config["SQL_RESOURCE"] = sql_resource
