from collections.abc import Iterator
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.core.settings import Settings
from app.core.sqlalchemy.context import Context
from app.infrastructure.sqlalchemy.utils import managed_session


@lru_cache
def get_settings() -> Settings:
    return Settings()  # ty: ignore[missing-argument]


def get_sql_session(request: Request) -> Iterator[Session]:
    with managed_session(request.app.state.sql_session_factory) as session:
        yield session


def get_context(sql_session: Annotated[Session, Depends(get_sql_session)]) -> Context:
    return Context(sql_session=sql_session)
