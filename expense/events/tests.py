from datetime import datetime, timedelta
from unittest.mock import patch

import pytest
from django.forms import ValidationError
from django.utils.text import slugify

from expense.events.forms import CreateEventForm


def test_create_event_form_clean_method_invalid():
    """
    CreateEventForm should raise a validation error if
    start_date is older that end_date
    """
    today = datetime.now()
    tomorrow = datetime.now() + timedelta(days=1)
    data = {
        "name": "event name",
        "start_date": tomorrow,
        "end_date": today,
    }

    form = CreateEventForm(user=None, data=data)

    assert not form.is_valid()
    with pytest.raises(ValidationError):
        form.clean()


def test_create_event_form_clean_method_valid():
    """
    CreateEventForm should raise return cleaned data if
    the data is valid
    """
    today = datetime.now()
    tomorrow = datetime.now() + timedelta(days=1)
    data = {
        "name": "event name",
        "start_date": today,
        "end_date": tomorrow,
    }

    form = CreateEventForm(user=None, data=data)

    assert form.is_valid()

    data = form.clean()

    assert data["end_date"]
    assert data["start_date"]
    assert data["name"]


class FakeEvent:
    def __init__(self) -> None:
        self.name = "fake_event"
        self.start_date = datetime.now()
        self.end_date = datetime.now() + timedelta(days=1)

    def save(self, commit=True):
        return self


@patch("expense.events.forms.ModelForm.save")
def test_create_event_form_save_method(mock_save):
    """
    If the form is valid, CreateEventForm.save should return an
    event object, with `slug` and `belongs_to` attirbutes set
    """
    mock_save.return_value = FakeEvent()

    today = datetime.now()
    tomorrow = datetime.now() + timedelta(days=1)
    data = {
        "name": "event name",
        "start_date": today,
        "end_date": tomorrow,
    }

    form = CreateEventForm(user="test-user", data=data)

    assert form.is_valid()

    event: FakeEvent = form.save()

    assert event.slug == f"{slugify(event.name)}-{event.start_date.strftime('%Y%m%d')}"
    assert event.belongs_to == "test-user"
