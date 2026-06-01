from collections.abc import Iterator
from typing import Annotated

from fast_depends import Depends
from flask import current_app
from sqlalchemy.orm import Session

from app.core.sqlalchemy.context import Context
from app.infrastructure.sqlalchemy.utils import managed_session


def get_sql_session() -> Iterator[Session]:
    with managed_session(current_app.config["SQL_SESSION_FACTORY"]) as session:
        yield session


def get_context(sql_session: Annotated[Session, Depends(get_sql_session)]) -> Context:
    return Context(sql_session=sql_session)
