from typing import Any, Dict
from django import forms

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

        if not available_balance or (available_balance < cleaned_data.get("amount")):
            raise forms.ValidationError(
                f"You don't have enough balance in {str(from_account)} account. Available balance is {available_balance}."
            )

        return cleaned_data
