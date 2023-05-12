from django.db import models
from django.utils import timezone

from expense.users.models import User


class AccountAction(models.Model):
    """
    Records the credit and debit actions that are done to the actual account.
    """

    class Action(models.TextChoices):
        CREDIT = "CREDIT", "Credit"
        DEBIT = "DEBIT", "Debit"

    description = models.CharField(max_length=255)
    amount = models.FloatField()
    action = models.TextField(
        choices=Action.choices,
        default=Action.CREDIT,
        max_length=255,
    )
    date = models.DateField(
        default=timezone.now
    )  # Since this is a tracking app, we want the user to specify when was the action done to their actual account

    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Indicate when was this action created

    belongs_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="account_actions",
    )

    class Meta:
        get_latest_by = "date"


class Account(models.Model):
    """
    Record the current amount of a user's account
    """

    amount = models.FloatField()
    action = models.OneToOneField(
        AccountAction,
        on_delete=models.CASCADE,
    )  # The action that created this account instance
    created_at = models.DateTimeField(auto_now_add=True)
    belongs_to = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        get_latest_by = "created_at"
