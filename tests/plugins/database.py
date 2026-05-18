from collections.abc import Iterator

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from app.core.settings import Settings
from app.infrastructure.sqlalchemy.models.base import OrmEntity


@pytest.fixture(scope="session")
def engine(app_settings: Settings) -> Engine:
    engine = create_engine(url=str(app_settings.postgres_dsn))

    OrmEntity.metadata.drop_all(engine)
    OrmEntity.metadata.create_all(engine)

    return engine


@pytest.fixture
def session(engine: Engine) -> Iterator[Session]:
    with Session(engine) as session:
        yield session

    with Session(engine) as session:
        for table in reversed(OrmEntity.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()
