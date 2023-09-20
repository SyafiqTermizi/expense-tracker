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

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        total_expense = (
            self.object.expense_set.values("event")
            .annotate(total_expense=Sum("expense__amount"))
            .order_by("total_expense")
            .values("total_expense")
            .first()
        ) or {"total_expense": 0}

        return {
            "expense": total_expense,
            "expenses": self.object.expense_set.select_related("expense"),
            **super().get_context_data(**kwargs),
        }


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
