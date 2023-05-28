from rest_framework import serializers
from rest_framework.relations import RelatedField

from expense.accounts.models import AccountAction
from expense.expenses.models import Expense


class AccountActionTypeField(RelatedField):
    def to_representation(self, obj: AccountAction) -> str:
        return obj.account_type.type.title()


class ExpenseSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    from_action = AccountActionTypeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format="%d/%m/%Y")

    class Meta:
        model = Expense
        fields = [
            "amount",
            "category",
            "created_at",
            "description",
            "from_action",
        ]


class AccountActionAndExpenseSerializer(serializers.ModelSerializer):
    expense = ExpenseSerializer(read_only=True)
    account_type = serializers.StringRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format="%d/%m/%Y")

    class Meta:
        model = AccountAction
        fields = [
            "expense",
            "account_type",
            "created_at",
            "description",
            "amount",
            "action",
        ]
