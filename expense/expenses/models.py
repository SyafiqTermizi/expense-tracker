from django.db import models
from django.urls import reverse

from expense.users.models import User
from expense.accounts.models import AccountAction


class Category(models.Model):
    """
    Expenses categories
    """

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120)
    belongs_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="expense_categories",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "belongs_to"],
                name="unique_category",
            )
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("expenses:categories:update", kwargs={"pk": self.pk})


class Expense(models.Model):
    """
    This model tracks what the expense is for and its category.
    """

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="expenses",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    from_action = models.OneToOneField(
        AccountAction,
        on_delete=models.CASCADE,
        related_name="expense",
    )
    belongs_to = models.ForeignKey(
        User,
        related_name="expenses",
        on_delete=models.CASCADE,
    )

    class Meta:
        get_latest_by = "created_at"


def get_upload_path(instance, filename):
    return f"{instance.expense.belongs_to.username}/{filename}"


class Image(models.Model):
    expense = models.ForeignKey(
        Expense,
        related_name="images",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to=get_upload_path)
