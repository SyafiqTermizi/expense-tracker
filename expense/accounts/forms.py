from typing import Any, Dict

from django import forms
from django.utils import timezone
from expense.users.models import User

from .models import AccountAction, Account, AccountType


class AccountActionForm(forms.ModelForm):
    """
    This form will automatically create related Account instance on save
    """

    class Meta:
        model = AccountAction
        fields = [
            "description",
            "action",
            "amount",
            "account_type",
            "belongs_to",
        ]

    def save(self, commit: bool):
        """
        Automatically create related Account instance
        """

        # Don't allow user/admin to update
        if self.instance.pk:
            return

        account_action: AccountAction = super().save(commit)
        account_action.save()
        new_amount = account_action.amount
        if account_action.action == AccountAction.Action.DEBIT:
            new_amount = account_action.amount * -1

        try:
            last_amount = (
                Account.objects.filter(
                    belongs_to=account_action.belongs_to,
                    action__account_type=account_action.account_type,
                )
                .latest("created_at")
                .amount
            )
        except Account.DoesNotExist:
            Account.objects.create(
                amount=new_amount,
                action=account_action,
                belongs_to=account_action.belongs_to,
            )
        else:
            Account.objects.create(
                amount=(last_amount + new_amount),
                action=account_action,
                belongs_to=account_action.belongs_to,
            )

        return account_action


class AccountTransferForm(forms.Form):
    from_account = forms.ModelChoiceField(
        queryset=AccountType.objects.all(),
        label="From Account",
    )
    to_account = forms.ModelChoiceField(
        queryset=AccountType.objects.all(),
        label="To Account",
    )
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    description = forms.CharField(max_length=255, required=False)

    def __init__(self, user: User, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["from_account"].queryset = user.account_types.all()
        self.fields["to_account"].queryset = user.account_types.all()

    def clean(self) -> Dict[str, Any]:
        fields = super().clean()
        if fields.get("from_account") == fields.get("to_account"):
            raise forms.ValidationError("Transfer to same account is not allowed")
        return fields

    def save(self):
        from_account = self.cleaned_data["from_account"]
        to_account = self.cleaned_data["to_account"]
        description = self.cleaned_data["description"]

        if not description:
            description = f"Transfer from {from_account.type} to {to_account.type}"

        amount = self.cleaned_data["amount"]

        AccountActionForm(
            data={
                "description": description,
                "action": AccountAction.Action.DEBIT,
                "amount": amount,
                "account_type": from_account,
                "belongs_to": self.user,
            }
        ).save(commit=True)

        AccountActionForm(
            data={
                "description": description,
                "action": AccountAction.Action.CREDIT,
                "amount": amount,
                "account_type": to_account,
                "belongs_to": self.user,
            }
        ).save(commit=True)


class WithdrawForm(forms.Form):
    from_account = forms.ModelChoiceField(
        queryset=AccountType.objects.all(),
        label="From Account",
    )
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    description = forms.CharField(max_length=255, required=False)

    def __init__(self, user: User, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["from_account"].queryset = user.account_types.exclude(
            type=AccountType.Type.CASH
        )

    def save(self):
        from_account = self.cleaned_data["from_account"]
        description = self.cleaned_data["description"]

        if not description:
            description = f"Withdrawal from {from_account.type}"

        amount = self.cleaned_data["amount"]

        AccountActionForm(
            data={
                "description": description,
                "action": AccountAction.Action.DEBIT,
                "amount": amount,
                "account_type": from_account,
                "belongs_to": self.user,
            }
        ).save(commit=True)

        AccountActionForm(
            data={
                "description": description,
                "action": AccountAction.Action.CREDIT,
                "amount": amount,
                "account_type": self.user.account_types.get(type=AccountType.Type.CASH),
                "belongs_to": self.user,
            }
        ).save(commit=True)
