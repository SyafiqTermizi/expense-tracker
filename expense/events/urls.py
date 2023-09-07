from django.urls import path

from .views import (
    CreateEventView,
    DeleteEventView,
    DetailEventView,
    ListEventView,
    UpdateEventView,
)

app_name = "events"
urlpatterns = [
    path("add", CreateEventView.as_view(), name="add"),
    path("delete/<slug:slug>", DeleteEventView.as_view(), name="delete"),
    path("detail/<slug:slug>", DetailEventView.as_view(), name="detail"),
    path("update/<slug:slug>", UpdateEventView.as_view(), name="update"),
    path("", ListEventView.as_view(), name="list"),
]
