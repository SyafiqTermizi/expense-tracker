from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CreateEventForm
from .models import Event


class CreateEventView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = CreateEventForm
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


class ListEventView(LoginRequiredMixin, ListView):
    model = Event

    def get_queryset(self) -> QuerySet[Any]:
        return self.request.user.events.order_by("-end_date")


class UpdateEventView(LoginRequiredMixin, UpdateView):
    form_class = CreateEventForm
    models = Event
    success_url = reverse_lazy("events:list")

    def get_form_kwargs(self) -> Dict[str, Any]:
        return {"user": self.request.user, **super().get_form_kwargs()}

    def get_queryset(self) -> QuerySet[Any]:
        return self.request.user.events.all()
