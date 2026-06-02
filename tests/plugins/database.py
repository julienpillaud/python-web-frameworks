from collections.abc import Iterator

import pytest
from sqlalchemy.orm import Session

from app.core.settings import Settings
from app.infrastructure.sqlalchemy.utils import SQLResource


@pytest.fixture(scope="session")
def sql_resource(app_settings: Settings) -> SQLResource:
    sql_resource = SQLResource.from_settings(app_settings)
    sql_resource.create_all()
    return sql_resource


@pytest.fixture
def session(sql_resource: SQLResource) -> Iterator[Session]:
    with sql_resource.session() as session:
        yield session

    sql_resource.reset()
