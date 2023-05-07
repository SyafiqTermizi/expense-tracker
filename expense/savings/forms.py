from django import forms

from .models import SavingAction, Saving


class SavingActionAdminForm(forms.ModelForm):
    class Meta:
        model = SavingAction
        fields = ["description", "amount", "date", "belongs_to"]

    def save(self, commit: bool):
        """
        Automatically create related Saving instance
        """

        # Don't allow user/admin to update
        if self.instance.pk:
            return

        saving_action: SavingAction = super().save(commit)
        saving_action.save()
        new_amount = saving_action.amount
        if saving_action.action == SavingAction.Action.DEBIT:
            new_amount = saving_action.amount * -1

        try:
            last_amount = (
                Saving.objects.filter(
                    belongs_to=saving_action.belongs_to,
                )
                .latest("created_at")
                .amount
            )
        except Saving.DoesNotExist:
            Saving.objects.create(
                amount=new_amount,
                action=saving_action,
                belongs_to=saving_action.belongs_to,
            )
        else:
            Saving.objects.create(
                amount=(last_amount + new_amount),
                action=saving_action,
                belongs_to=saving_action.belongs_to,
            )

        return saving_action
