from app.api.fastapi.app import create_fastapi_app
from app.core.settings import Settings

settings = Settings()
app = create_fastapi_app(settings=settings)
