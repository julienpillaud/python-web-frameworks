from flask import Flask

from app.api.flask.dependencies import sql_session_teardown
from app.core.settings import Settings
from app.infrastructure.sqlalchemy.utils import create_sql_resource


def init_app(settings: Settings, app: Flask) -> None:
    sql_resource = create_sql_resource(settings=settings)
    app.config["SQL_ENGINE"] = sql_resource.engine
    app.config["SQL_SESSION_FACTORY"] = sql_resource.session_factory

    app.teardown_appcontext(sql_session_teardown)
