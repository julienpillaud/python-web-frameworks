from flask import Flask

from app.api.flask.dev.router import router as dev_router
from app.api.flask.exceptions import add_exception_handlers
from app.api.flask.items.router import router as items_router
from app.api.flask.utils import init_app
from app.core.settings import Settings


def create_flask_app(settings: Settings) -> Flask:
    app = Flask(__name__)

    add_exception_handlers(app=app)
    app.register_blueprint(items_router)
    app.register_blueprint(dev_router)
    init_app(settings=settings, app=app)

    return app
