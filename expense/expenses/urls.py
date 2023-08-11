from django.urls import path, include

from .views import (
    add_expense_view,
    monthly_expense_detail_view,
    add_expense_category,
    list_expense_categories,
    update_expense_categories,
    delete_expense_categories,
    expense_detail_api_view,
)

app_name = "expenses"

categories = (
    [
        path("add", add_expense_category, name="add"),
        path("list", list_expense_categories, name="list"),
        path("update/<slug:slug>", update_expense_categories, name="update"),
        path("delete/<slug:slug>", delete_expense_categories, name="delete"),
    ],
    "categories",
)

urlpatterns = [
    path("add", add_expense_view, name="add"),
    path("monthly", monthly_expense_detail_view, name="detail"),
    path("detail/<int:pk>", expense_detail_api_view),
    path("categories/", include(categories), name="categories"),
]
