from django.urls import path, include

from .views import (
    add_expense_view,
    add_expense_category,
    list_expense_categories,
    update_expense_categories,
    delete_expense_categories,
)

app_name = "expenses"

categories = (
    [
        path("add", add_expense_category, name="add"),
        path("list", list_expense_categories, name="list"),
        path("update/<int:pk>", update_expense_categories, name="update"),
        path("delete/<int:pk>", delete_expense_categories, name="delete"),
    ],
    "categories",
)

urlpatterns = [
    path("add", add_expense_view, name="add"),
    path("categories/", include(categories), name="categories"),
]
