from django.urls import path

from .views import transfer_view, add_view, detail_view

app_name = "accounts"
urlpatterns = [
    path("add", add_view, name="add_view"),
    path("transfer", transfer_view, name="transfer_view"),
    path("<slug:slug>", detail_view, name="detail_view"),
]
