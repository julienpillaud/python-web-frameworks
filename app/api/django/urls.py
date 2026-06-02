from django.urls import path
from django.urls.resolvers import URLPattern, URLResolver

from app.api.django.handlers import custom_handler404
from app.api.django.items.routes import (
    DevEnvView,
    DevErrorView,
    ItemView,
    ItemViewDetail,
)

urlpatterns: list[URLPattern | URLResolver] = [
    path("items", ItemView.as_view()),
    path("items/<item_id>", ItemViewDetail.as_view()),
    path("dev/env", DevEnvView.as_view()),
    path("dev/error", DevErrorView.as_view()),
]

# Override handler to return JSON response
handler404 = custom_handler404
