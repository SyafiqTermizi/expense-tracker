from django.db import models
from django.urls import reverse

from expense.users.models import User


class Account(models.Model):
    """
    Record accounts that a user have
    """

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    belongs_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="accounts",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "belongs_to"],
                name="unique_account",
            ),
            models.UniqueConstraint(
                fields=["slug", "belongs_to"],
                name="unique_slug",
            ),
        ]

    def __str__(self):
        return self.name.title()

    def get_absolute_url(self):
        return reverse("accounts:detail_view", kwargs={"slug": self.slug})


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
    account = models.ForeignKey(
        Account,
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


class AccountBalance(models.Model):
    """
    Record the current amount of a user's account
    """

    amount = models.FloatField()
    action = models.OneToOneField(
        AccountAction,
        on_delete=models.CASCADE,
    )  # The action that created this account instance
    created_at = models.DateTimeField(auto_now_add=True)
    belongs_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="account_balances",
    )

    class Meta:
        get_latest_by = "created_at"

    @property
    def account(self):
        return self.action.account.name
