from django.apps import AppConfig
from django.db.models.signals import post_save

from .signals import create_account_for_newly_created_user


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "expense.accounts"

    def ready(self) -> None:
        post_save.connect(
            create_account_for_newly_created_user,
            sender="users.User",
        )
