from django.db import models
from django.utils import timezone

from expense.expenses.models import Expense as UserExpense
from expense.users.models import User


class Event(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120)
    belongs_to = models.ForeignKey(
        User,
        related_name="events",
        on_delete=models.CASCADE,
    )

    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["slug", "belongs_to"],
                name="unique_event_slug",
            ),
        ]

    def __str__(self) -> str:
        return self.name

    @property
    def active(self):
        return self.end_date > timezone.localtime(timezone.now()).date()


class Expense(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    expense = models.ForeignKey(
        UserExpense,
        related_name="expenses",
        on_delete=models.CASCADE,
    )

    # User will be able to create an expense and add it to an event later
    created_at = models.DateTimeField(auto_now_add=True)
