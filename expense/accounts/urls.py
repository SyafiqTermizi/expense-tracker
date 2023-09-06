from django.urls import path

from .views import (
    add_view,
    CreateAccountView,
    DeleteAccountView,
    MontlyAccountDetailView,
    TransferView,
    UpdateAccountView,
)

app_name = "accounts"
urlpatterns = [
    path("add", add_view, name="add_view"),
    path("transfer", TransferView.as_view(), name="transfer_view"),
    path("create", CreateAccountView.as_view(), name="create_view"),
    path("delete/<slug:slug>", DeleteAccountView.as_view(), name="delete_view"),
    path("update/<slug:slug>", UpdateAccountView.as_view(), name="update_view"),
    path("detail/<slug:slug>", MontlyAccountDetailView.as_view(), name="detail_view"),
]
