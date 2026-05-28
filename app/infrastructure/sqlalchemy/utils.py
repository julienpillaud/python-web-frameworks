from collections.abc import Iterator
from contextlib import contextmanager

from pydantic import BaseModel, ConfigDict
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.core.settings import Settings
from app.infrastructure.sqlalchemy.logger import logger
from app.infrastructure.sqlalchemy.models.base import OrmEntity


class SQLResource(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    engine: Engine
    session_factory: sessionmaker[Session]

    def release(self) -> None:
        logger.info("SQL engine released")
        self.engine.dispose()

    def reset(self) -> None:
        with self.session_factory() as session:
            for table in reversed(OrmEntity.metadata.sorted_tables):
                session.execute(table.delete())
            session.commit()


def create_sql_resource(settings: Settings) -> SQLResource:
    engine = create_engine(
        url=str(settings.postgres_dsn),
        **settings.postgres_params,
    )
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    logger.info("SQL engine up")
    return SQLResource(
        engine=engine,
        session_factory=sessionmaker(bind=engine),
    )


@contextmanager
def managed_session(session_factory: sessionmaker[Session]) -> Iterator[Session]:
    session = session_factory()
    try:
        yield session
        session.commit()
        logger.info("Commit ok")
    except Exception as error:
        logger.error(f"Rollback due to {error}")
        session.rollback()
        raise
    finally:
        session.close()
