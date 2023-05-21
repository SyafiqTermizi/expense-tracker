from django.urls import path

from .views import add_expense_view

app_name = "expenses"
urlpatterns = [
    path("add", add_expense_view, name="add_view"),
]
