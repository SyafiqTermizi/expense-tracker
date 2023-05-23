from django.apps import AppConfig
from django.db.models.signals import post_save

from .signals import create_expense_category_for_newly_created_user


class ExpensesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "expense.expenses"

    def ready(self) -> None:
        post_save.connect(
            create_expense_category_for_newly_created_user,
            sender="users.User",
        )
