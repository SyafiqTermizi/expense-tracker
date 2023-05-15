from django.urls import path

from .views import dashboard_view, transfer_view, add_view

app_name = "accounts"
urlpatterns = [
    path("", dashboard_view, name="dashboard_view"),
    path("add", add_view, name="add_view"),
    path("transfer", transfer_view, name="transfer_view"),
]
