from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.api.dependencies import get_settings
from app.core.settings import Settings
from app.core.sqlalchemy.context import Context


def get_sql_session(request: Request) -> Iterator[Session]:
    with request.app.state.sql_resource.session() as session:
        yield session


def get_context(
    settings: Annotated[Settings, Depends(get_settings)],
    sql_session: Annotated[Session, Depends(get_sql_session)],
) -> Context:
    return Context(settings=settings, sql_session=sql_session)
