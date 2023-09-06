from django.urls import path

from .views import CreateEventView, DeleteEventView, ListEventView

app_name = "events"
urlpatterns = [
    path("add", CreateEventView.as_view(), name="add"),
    path("delete/<slug:slug>", DeleteEventView.as_view(), name="delete"),
    path("", ListEventView.as_view(), name="list"),
]
