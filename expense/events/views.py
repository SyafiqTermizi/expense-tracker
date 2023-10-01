from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from expense.expenses.models import Expense as UserExpense
from expense.expenses.utils import get_formatted_user_expense_for_month

from .forms import EventForm
from .models import Event


class CreateEventView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    success_url = reverse_lazy("events:list")

    def get_form_kwargs(self) -> Dict[str, Any]:
        return {"user": self.request.user, **super().get_form_kwargs()}


class DeleteEventView(LoginRequiredMixin, DeleteView):
    success_url = success_url = reverse_lazy("events:list")

    def get_queryset(self) -> QuerySet[Any]:
        return self.request.user.events.all()


class DetailEventView(LoginRequiredMixin, DetailView):
    model = Event

    def get_queryset(self) -> QuerySet[Any]:
        return self.request.user.events.all()

    def get_expense_by_category_context(self):
        expense_by_category = {}
        for category_expense in self.object.expense_set.values(
            "expense__category__name"
        ).annotate(total=Sum("expense__amount")):
            expense_by_category.update(
                {category_expense["expense__category__name"]: category_expense["total"]}
            )

        return expense_by_category

    def get_expense_this_month_context(self, expense_ids: list[int]):
        return get_formatted_user_expense_for_month(
            UserExpense.objects.filter(pk__in=expense_ids)
            .order_by("-created_at")
            .values(
                "slug",
                "from_action__account__name",
                "created_at",
                "description",
                "amount",
                "category__name",
            )
        )

    def expense_by_account_context(self, expense_ids: list[int]):
        expense_by_account = {}
        for account_expense in (
            UserExpense.objects.filter(pk__in=expense_ids)
            .values("from_action__account__name")
            .annotate(total=Sum("amount"))
        ):
            expense_by_account.update(
                {
                    account_expense["from_action__account__name"]: account_expense[
                        "total"
                    ]
                }
            )
        return expense_by_account

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        expense_ids = list(
            self.object.expense_set.values_list("expense__pk", flat=True)
        )

        if not expense_ids:
            # Return early to prevent unecessary DB query
            return super().get_context_data(**kwargs)

        total_expense = (
            self.object.expense_set.values("event")
            .annotate(total=Sum("expense__amount"))
            .order_by("total")
            .values("total")
            .first()
        ) or {"total": 0}

        context = {
            "total_expense": total_expense,
            "expense_by_account": self.expense_by_account_context(
                expense_ids=expense_ids
            ),
            "expense_by_category": self.get_expense_by_category_context(),
            "expenses": self.get_expense_this_month_context(expense_ids),
            **super().get_context_data(**kwargs),
        }

        if self.object.active:
            context.update({"active_event": {"slug": self.object.slug}})

        return context


class ListEventView(LoginRequiredMixin, ListView):
    model = Event

    def get_queryset(self) -> QuerySet[Any]:
        return self.request.user.events.order_by("-end_date")


class UpdateEventView(LoginRequiredMixin, UpdateView):
    form_class = EventForm
    models = Event
    success_url = reverse_lazy("events:list")

    def get_form_kwargs(self) -> Dict[str, Any]:
        return {"user": self.request.user, **super().get_form_kwargs()}

    def get_queryset(self) -> QuerySet[Any]:
        return self.request.user.events.all()
