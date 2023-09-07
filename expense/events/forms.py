from typing import Any, Dict

from django import forms
from django.forms import ModelForm
from django.utils.text import slugify

from expense.users.models import User

from .models import Event


class CreateEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["name", "start_date", "end_date"]

    def __init__(self, user: User, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()

        if cleaned_data["start_date"] > cleaned_data["end_date"]:
            raise forms.ValidationError("Start date can't be earlier than end date")

        return cleaned_data

    def save(self) -> Any:
        event: Event = super().save(commit=False)
        event.slug = f"{slugify(event.name)}-{event.start_date.strftime('%Y%m%d')}"
        event.belongs_to = self.user

        event.save()

        return event
