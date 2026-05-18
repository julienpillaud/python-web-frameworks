from django.urls import path
from django.urls.resolvers import URLPattern, URLResolver

from app.api.django.items.routes import ItemView, ItemViewDetail

urlpatterns: list[URLPattern | URLResolver] = [
    path("items", ItemView.as_view()),
    path("items/<item_id>", ItemViewDetail.as_view()),
]
