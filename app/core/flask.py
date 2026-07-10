from app.api.flask.app import create_flask_app
from app.core.settings import Settings

settings = Settings()
app = create_flask_app(settings=settings)
