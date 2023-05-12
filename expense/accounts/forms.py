from django import forms

from .models import AccountAction, Account


class AccountActionAdminForm(forms.ModelForm):
    class Meta:
        model = AccountAction
        fields = ["description", "amount", "date", "belongs_to"]

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
