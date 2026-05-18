from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy.orm import Session, sessionmaker

from app.infrastructure.sqlalchemy.logger import logger


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
