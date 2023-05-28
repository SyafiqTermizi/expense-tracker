from django.db import models
from django.utils import timezone

from expense.users.models import User


class AccountType(models.Model):
    """
    Record the type of account that a user has
    """

    class Type(models.TextChoices):
        INCOME = "INCOME", "Income"
        SAVING = "SAVING", "Saving"
        CASH = "CASH", "Cash"
        OTHER = "OTHER", "Other"

    type = models.TextField(
        choices=Type.choices,
        default=Type.OTHER,
        max_length=255,
    )
    description = models.CharField(max_length=255)
    belongs_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="account_types",
    )

    def __str__(self):
        return self.type.title()


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
    account_type = models.ForeignKey(
        AccountType,
        on_delete=models.CASCADE,
        related_name="actions",
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Indicate when was this action created

    belongs_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="account_actions",
    )

    class Meta:
        get_latest_by = "created_at"


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

    @property
    def type(self):
        return self.action.account_type.type
