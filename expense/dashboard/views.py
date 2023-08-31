from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone

from expense.accounts.utils import (
    get_latest_account_balance,
    get_transactions_with_expense_data,
)
from expense.types import AccountBalance


def user_is_new(
    account_balance: list[AccountBalance],
    transactions: list,
    expenses: list,
) -> bool:
    """
    Check if the user is new by checking if the user:
    - Has made an account balance
    - Transactions
    - Expenses
    """
    return all(
        [
            sum(list(map(lambda acc: acc["balance"], account_balance))) == 0,
            len(transactions) == 0,
            len(expenses) == 0,
        ]
    )


@login_required
def dashboard_view(request: HttpRequest) -> HttpResponse:
    """
    Returns an overview of the user's account balance and spendings
    """

    # 1. Get data to display on the dashboard
    accounts = get_latest_account_balance(request.user)

    transactions = get_transactions_with_expense_data(
        request.user,
        timezone.localtime(timezone.now()).month,
        timezone.localtime(timezone.now()).year,
        account=None,
    )

    expenses = list(
        map(
            lambda expense: {
                "category": expense["category__name"],
                "amount": expense["amount"],
            },
            request.user.expenses.filter(
                created_at__month=timezone.localtime(timezone.now()).month,
                created_at__year=timezone.localtime(timezone.now()).year,
            )
            .values("category__name")
            .annotate(amount=Sum("amount")),
        )
    )

    # 2. Render an empty page that will user to create new balance, it the user is new
    if user_is_new(accounts, transactions, expenses):
        return render(request=request, template_name="dashboard/empty_partial.html")

    return render(
        request,
        "dashboard/dashboard.html",
        context={
            "accounts": accounts,
            "transactions": transactions,
            "expenses": expenses,
        },
    )
