from flask import current_app, g

from app.core.sqlalchemy.context import Context


def get_context() -> Context:
    if "sql_session" not in g:
        sql_session_factory = current_app.config["SQL_SESSION_FACTORY"]
        g.sql_session = sql_session_factory()

    return Context(sql_session=g.sql_session)


def sql_session_teardown(error: BaseException | None) -> None:
    sql_session = g.pop("sql_session", None)
    if sql_session is not None:
        if error is not None:
            sql_session.rollback()
        else:
            sql_session.commit()
        sql_session.close()
