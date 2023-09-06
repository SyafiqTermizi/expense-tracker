import calendar
from typing import Any, Dict

from django import forms
from django.utils import timezone
from expense.accounts.models import AccountBalance
from expense.users.models import User


class BaseFromAccountForm(forms.Form):
    """
    This form declares from_account as one of its field and does the validation
    """

    def __init__(self, user: User, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user = user

        self.fields["from_account"] = forms.ModelChoiceField(
            queryset=user.accounts.all(),
            to_field_name="slug",
        )

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        from_account = cleaned_data.get("from_account")

        try:
            available_balance = (
                AccountBalance.objects.filter(action__account=from_account)
                .latest()
                .amount
            )
        except AccountBalance.DoesNotExist:
            available_balance = 0

        if not available_balance or (available_balance < cleaned_data.get("amount", 0)):
            raise forms.ValidationError(
                f"You don't have enough balance in {str(from_account)} account. Available balance is {available_balance}."
            )

        return cleaned_data


class MonthQueryParamForm(forms.Form):
    month = forms.IntegerField(min_value=1, max_value=12)
    year = forms.IntegerField(min_value=2022, max_value=2100)

    def get_month_name(self):
        """
        Returns month name if the given month is valid, else return None
        """
        try:
            month_int = self.cleaned_data["month"]
        except KeyError:
            return

        return calendar.month_name[month_int]


def get_localtime_kwargs(query_kwargs=False):
    time_obj = timezone.localtime(timezone.now())
    if query_kwargs:
        return {
            "created_at__month": time_obj.month,
            "created_at__year": time_obj.year,
        }
    return {
        "month": time_obj.month,
        "year": time_obj.year,
    }
