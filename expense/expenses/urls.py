from django.urls import include, path

from .views.categories import (
    CreateCategoryView,
    DeleteCategoryView,
    ListCategoryView,
    UpdateCategoryView,
)
from .views.expense import (
    MonthlyExpenseDetailView,
    add_expense_view,
    expense_detail_api_view,
    update_expense_view,
)

app_name = "expenses"

categories = (
    [
        path("add", CreateCategoryView.as_view(), name="add"),
        path("list", ListCategoryView.as_view(), name="list"),
        path("update/<slug:slug>", UpdateCategoryView.as_view(), name="update"),
        path("delete/<slug:slug>", DeleteCategoryView.as_view(), name="delete"),
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
