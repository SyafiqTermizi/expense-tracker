from django.urls import include, path

from .views import (
    MonthlyExpenseDetailView,
    add_expense_category,
    add_expense_view,
    delete_expense_categories,
    expense_detail_api_view,
    list_expense_categories,
    update_expense_categories,
    update_expense_view,
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
    path("update/<slug:slug>", update_expense_view, name="update"),
    path("monthly", MonthlyExpenseDetailView.as_view(), name="detail"),
    path("detail/<slug:slug>", expense_detail_api_view),
    path("categories/", include(categories), name="categories"),
]
