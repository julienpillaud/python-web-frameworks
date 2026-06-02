from collections.abc import Iterator
from typing import Annotated

from fast_depends import Depends
from flask import current_app
from sqlalchemy.orm import Session

from app.api.dependencies import get_settings
from app.core.settings import Settings
from app.core.sqlalchemy.context import Context


def get_sql_session() -> Iterator[Session]:
    with current_app.config["SQL_RESOURCE"].session() as session:
        yield session


def get_context(
    settings: Annotated[Settings, Depends(get_settings)],
    sql_session: Annotated[Session, Depends(get_sql_session)],
) -> Context:
    return Context(settings=settings, sql_session=sql_session)
