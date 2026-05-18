from django.conf import settings
from django.core.wsgi import get_wsgi_application

from app.core.settings import Settings

app_settings = Settings()  # ty: ignore[missing-argument]
settings.configure(
    DEBUG=app_settings.django.debug,
    SECRET_KEY=app_settings.django.secret_key,
    ROOT_URLCONF=app_settings.django.root_urlconf,
    INSTALLED_APPS=app_settings.django.installed_apps,
    MIDDLEWARE=app_settings.django.middleware,
    DATABASES={"default": app_settings.django_postgres},
)

app = get_wsgi_application()
