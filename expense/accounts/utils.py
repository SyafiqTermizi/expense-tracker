from django.utils.crypto import get_random_string

from expense.accounts.models import Account
from expense.expenses.models import Image as ExpenseImage
from expense.users.models import User


def get_actions_with_expense_data(
    user: User,
    month: int,
    year: int,
    account: Account = None,
):
    """
    Retrieve all actions for a given month and year along with expenses
    """
    action_filter_kwargs = {
        "created_at__month": month,
        "created_at__year": year,
    }
    if account:
        action_filter_kwargs.update({"account": account})

    account_actions = (
        user.account_actions.filter(**action_filter_kwargs)
        .order_by("-created_at")
        .select_related("expense", "account", "expense__category")
    )

    expense_image_mapping = {}
    for image in ExpenseImage.objects.filter(
        expense__created_at__month=month,
        expense__created_at__year=year,
        expense__belongs_to=user,
    ).select_related("expense"):
        expense_image_mapping.update({image.expense.pk: image.image.url})

    transactions = []
    for action in account_actions:
        data = {
            "account": str(action.account),
            "created_at": action.created_at,
            "description": action.description,
            "amount": action.amount,
            "action": action.action,
        }

        if hasattr(action, "expense"):
            data.update(
                {
                    "expense": True,
                    "image": expense_image_mapping.get(action.expense.pk),
                    "uid": get_random_string(10),
                    "category": action.expense.category.name,
                }
            )

        transactions.append(data)

    return transactions


def get_latest_account_balance(user: User):
    """
    Get latest balance for all accounts for a given user
    """
    # 1. Get account balance
    accounts = []
    for balance in (
        user.account_balances.order_by(
            "action__account__name",
            "-created_at",
        )
        .select_related("action__account")
        .distinct("action__account__name")
    ):
        accounts.append(
            {
                "name": balance.action.account.name,
                "balance": balance.amount,
                "url": balance.action.account.get_absolute_url(),
                "slug": balance.action.account.slug,
            }
        )

    # 1.1 Add accounts with no balance
    for account in user.accounts.exclude(
        name__in=list(map(lambda acc: acc["name"], accounts))
    ):
        accounts.append(
            {
                "name": account.name,
                "balance": 0,
                "url": account.get_absolute_url(),
                "slug": account.slug,
            }
        )

    return accounts
