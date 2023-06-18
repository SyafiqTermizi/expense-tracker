from django.urls import path, include

from .views import add_expense_view, add_expense_category

app_name = "expenses"

categories = (
    [
        path("add", add_expense_category, name="add"),
    ],
    "categories",
)

urlpatterns = [
    path("add", add_expense_view, name="add"),
    path("categories/", include(categories), name="categories"),
]
