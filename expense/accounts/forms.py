from typing import Any, Dict

from django import forms
from django.utils.text import slugify

from expense.users.models import User
from expense.utils import BaseFromAccountForm

from .models import Account, AccountAction, AccountBalance


class AccountActionForm(forms.ModelForm):
    """
    This form will automatically create related Account instance on save
    """

    def __init__(self, user: User, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["account"] = forms.ModelChoiceField(
            queryset=user.accounts.all(),
            to_field_name="slug",
        )

    class Meta:
        model = AccountAction
        fields = [
            "description",
            "action",
            "amount",
            "account",
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
                AccountBalance.objects.filter(
                    belongs_to=account_action.belongs_to,
                    action__account=account_action.account,
                )
                .latest("created_at")
                .amount
            )
        except AccountBalance.DoesNotExist:
            last_amount = 0

        AccountBalance.objects.create(
            amount=(last_amount + new_amount),
            action=account_action,
            belongs_to=account_action.belongs_to,
        )

        return account_action


class AccountTransferForm(BaseFromAccountForm):
    """
    Transfer money from one account to another
    """

    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    description = forms.CharField(max_length=255, required=False)

    def __init__(self, user: User, *args, **kwargs) -> None:
        super().__init__(user, *args, **kwargs)

        self.fields["to_account"] = forms.ModelChoiceField(
            queryset=user.accounts.all(),
            to_field_name="slug",
        )

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()

        if cleaned_data.get("from_account") == cleaned_data.get("to_account"):
            raise forms.ValidationError("Transfer to same account is not allowed")

        return cleaned_data

    def save(self):
        from_account = self.cleaned_data["from_account"]
        to_account = self.cleaned_data["to_account"]
        description = self.cleaned_data["description"]

        if not description:
            description = f"Transfer from {str(from_account)} to {str(to_account)}"

        amount = self.cleaned_data["amount"]

        AccountActionForm(
            user=self.user,
            data={
                "description": description,
                "action": AccountAction.Action.DEBIT,
                "amount": amount,
                "account": from_account,
                "belongs_to": self.user,
            },
        ).save(commit=True)

        AccountActionForm(
            user=self.user,
            data={
                "description": description,
                "action": AccountAction.Action.CREDIT,
                "amount": amount,
                "account": to_account,
                "belongs_to": self.user,
            },
        ).save(commit=True)


class AccountForm(forms.ModelForm):
    initial_balance = forms.DecimalField(required=False)

    def __init__(self, user: User, *args, **kwargs) -> None:
        self.user = user
        super().__init__(*args, **kwargs)

    class Meta:
        model = Account
        fields = ["name", "description"]

    def save(self) -> Any:
        account = super().save(commit=False)
        account.belongs_to = self.user
        account.slug = slugify(account.name)
        account.save()

        if amount := self.cleaned_data["initial_balance"]:
            AccountActionForm(
                user=self.user,
                data={
                    "description": f"{account.name.title()} initial balance",
                    "action": AccountAction.Action.CREDIT,
                    "amount": amount,
                    "account": account,
                    "belongs_to": self.user,
                },
            ).save(commit=True)

        return account
