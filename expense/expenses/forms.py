from typing import Any, Dict
from django import forms

from expense.accounts.forms import AccountActionForm
from expense.accounts.models import AccountAction
from expense.users.models import User

from .models import Expense


class AddExpenseForm(forms.Form):
    """
    Deduct money from an account and Create a new expense instance
    """

    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    description = forms.CharField(max_length=255, required=False)

    def __init__(self, user: User, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user = user

        # Fields
        self.fields["category"] = forms.ModelChoiceField(
            queryset=user.expense_categories.all(),
            required=False,
        )
        self.fields["from_account"] = forms.ModelChoiceField(
            queryset=user.account_types.all()
        )

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        if not cleaned_data.get("category") and not cleaned_data.get("description"):
            raise forms.ValidationError("Either category or description is required")
        return cleaned_data

    def save(self):
        from_account = self.cleaned_data["from_account"]
        description = self.cleaned_data["description"]
        category = self.cleaned_data["category"]
        amount = self.cleaned_data["amount"]

        if not description:
            description = f"{category.name} expenses"

        account_action = AccountActionForm(
            data={
                "description": description,
                "action": AccountAction.Action.DEBIT,
                "amount": amount,
                "account_type": from_account,
                "belongs_to": self.user,
            }
        ).save(commit=True)

        return Expense.objects.create(
            amount=amount,
            category=category,
            description=description,
            from_action=account_action,
            belongs_to=self.user,
        )
