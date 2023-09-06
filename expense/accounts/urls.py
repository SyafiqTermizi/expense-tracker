from django.urls import path

from .views import (
    add_view,
    create_account_view,
    delete_account_view,
    MontlyAccountDetailView,
    transfer_view,
    update_account_view,
)

app_name = "accounts"
urlpatterns = [
    path("add", add_view, name="add_view"),
    path("transfer", transfer_view, name="transfer_view"),
    path("create", create_account_view, name="create_view"),
    path("delete/<slug:slug>", delete_account_view, name="delete_view"),
    path("update/<slug:slug>", update_account_view, name="update_view"),
    path("detail/<slug:slug>", MontlyAccountDetailView.as_view(), name="detail_view"),
]
