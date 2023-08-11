from expense.accounts.models import Account
from expense.types import AccountBalance
from expense.users.models import User


def get_transactions_with_expense_data(
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

    # 1. Get all user's account actions
    account_actions = (
        user.account_actions.filter(**action_filter_kwargs)
        .order_by("-created_at")
        .select_related("expense", "account", "expense__category")
    )

    transactions = []
    for action in account_actions:
        data = {
            "account": str(action.account),
            "created_at": action.created_at,
            "description": action.description,
            "amount": action.amount,
            "action": action.action,
        }

        # 3. If that action is an expense, attach the image
        if hasattr(action, "expense"):
            data.update(
                {
                    "expense": True,
                    "id": action.expense.slug,
                    "category": action.expense.category.name,
                }
            )

        transactions.append(data)

    return transactions


def get_latest_account_balance(user: User) -> list[AccountBalance]:
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
