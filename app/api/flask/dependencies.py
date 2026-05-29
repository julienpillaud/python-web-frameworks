from flask import current_app, g

from app.core.sqlalchemy.context import Context
from app.infrastructure.sqlalchemy.logger import logger


def get_context() -> Context:
    if "sql_session" not in g:
        sql_session_factory = current_app.config["SQL_SESSION_FACTORY"]
        g.sql_session = sql_session_factory()

    return Context(sql_session=g.sql_session)


def sql_session_teardown(error: BaseException | None) -> None:
    # In Flask, `error` is only set for unhandled exceptions
    # The global Exception handler catches everything, so `error` is always None.

    sql_session = g.pop("sql_session", None)
    if not sql_session:
        return

    if g.pop("error", None):
        logger.error(f"Rollback due to '{g.exception}'")
        sql_session.rollback()
        sql_session.close()
        return

    sql_session.commit()
    logger.info("Commit ok")
    sql_session.close()
