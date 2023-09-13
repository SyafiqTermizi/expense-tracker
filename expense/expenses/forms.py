from typing import Any, Dict

from django import forms
from django.utils.text import slugify

from expense.accounts.forms import AccountActionForm
from expense.accounts.models import AccountAction
from expense.events.models import Event, Expense as EventExpense
from expense.users.models import User
from expense.utils import BaseFromAccountForm

from .models import Category, Expense, Image


class AddExpenseForm(BaseFromAccountForm):
    """
    Deduct money from an account and Create a new expense instance
    """

    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    description = forms.CharField(max_length=255, required=False)

    image = forms.ImageField(required=False)

    def __init__(self, user: User, *args, **kwargs) -> None:
        super().__init__(user, *args, **kwargs)

        # fields that requires query that relates to user
        self.fields.update(
            {
                "category": forms.ModelChoiceField(
                    queryset=user.expense_categories.all(),
                    to_field_name="slug",
                ),
                "event": forms.ModelChoiceField(
                    queryset=Event.objects.get_user_active_events(user),
                    required=False,
                    to_field_name="slug",
                ),
            }
        )

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()

        if not cleaned_data.get("category") and not cleaned_data.get("description"):
            raise forms.ValidationError("Either category or description is required")

        return cleaned_data

    def save(self):
        description = self.cleaned_data["description"]
        category = self.cleaned_data["category"]
        amount = self.cleaned_data["amount"]

        if not description:
            description = f"{category.name} expenses"

        account_action = AccountActionForm(
            user=self.user,
            data={
                "description": description,
                "action": AccountAction.Action.DEBIT,
                "amount": amount,
                "account": self.cleaned_data["from_account"],
                "belongs_to": self.user,
            },
        ).save(commit=True)

        expense = Expense.objects.create(
            amount=amount,
            category=category,
            description=description,
            from_action=account_action,
            belongs_to=self.user,
        )

        if image := self.cleaned_data.get("image"):
            Image.objects.create(expense=expense, image=image)

        if event := self.cleaned_data.get("event"):
            EventExpense.objects.create(event=event, expense=expense)

        return expense


class UpdateExpenseForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Expense
        fields = ["category", "description"]

    def __init__(self, user: User, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["category"] = forms.ModelChoiceField(
            queryset=user.expense_categories.all(),
            to_field_name="slug",
        )

    def save(self) -> Any:
        expense: Expense = super().save(commit=True)
        expense_image: Image = expense.images.first()
        uploaded_image = self.cleaned_data.get("image")

        if uploaded_image and expense_image:
            expense_image.image = uploaded_image
            expense_image.save()

        if uploaded_image and not expense_image:
            Image.objects.create(expense=expense, image=uploaded_image)

        return expense


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)

    def __init__(self, user: User, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self) -> Any:
        category = super().save(commit=False)
        category.belongs_to = self.user
        category.slug = slugify(category.name)
        category.save()

        return category
