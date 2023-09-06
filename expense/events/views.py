from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models.query import QuerySet
from django.views.generic import CreateView, DeleteView, ListView
from django.urls import reverse_lazy

from .forms import CreateEventForm
from .models import Event


class CreateEventView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = CreateEventForm
    success_url = reverse_lazy("events:list")

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs


class ListEventView(LoginRequiredMixin, ListView):
    model = Event

    def get_queryset(self) -> QuerySet[Any]:
        return self.request.user.events.all()


class DeleteEventView(LoginRequiredMixin, DeleteView):
    success_url = success_url = reverse_lazy("events:list")

    def get_queryset(self) -> QuerySet[Any]:
        return self.request.user.events.all()
