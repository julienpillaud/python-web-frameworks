from django.apps import AppConfig

DJANGO_APPS = [
    "app.infrastructure.django.apps.DjangoApp",
]


class DjangoApp(AppConfig):
    name = "app.infrastructure.django"
