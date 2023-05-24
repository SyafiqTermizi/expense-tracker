from django.urls import path

from .views import transfer_view, add_view

app_name = "accounts"
urlpatterns = [
    path("add", add_view, name="add_view"),
    path("transfer", transfer_view, name="transfer_view"),
    # path("withdraw", withdraw_view, name="withdraw_view"),
]
