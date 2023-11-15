from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone

from expense.accounts.utils import (
    get_latest_account_balance,
    get_transactions_with_expense_data,
)
from expense.events.models import Event
from expense.types import AccountBalance
from expense.users.models import User
from expense.utils import get_localtime_kwargs


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


def get_formatted_active_events(user: User) -> list[dict]:
    """Returns a list of dict of active events"""
    active_events = (
        Event.objects.get_user_active_events(user)
        .values("pk")
        .annotate(total=Sum("expense__expense__amount"))
        .values("slug", "total", "name", "start_date", "end_date")
    )
    for event in active_events:
        total_days = (event["end_date"] - event["start_date"]).days
        current_days = (
            timezone.localtime(timezone.now()).date() - event["start_date"]
        ).days
        event.update({"percent_complete": (current_days / total_days) * 100})
    return active_events


@login_required
def dashboard_view(request: HttpRequest) -> HttpResponse:
    """
    Returns an overview of the user's account balance and spendings
    """

    # 1. Get data to display on the dashboard
    accounts = get_latest_account_balance(request.user)

    transactions = get_transactions_with_expense_data(
        user=request.user,
        account=None,
        **get_localtime_kwargs(),
    )

    expenses = list(
        map(
            lambda expense: {
                "category": expense["category__name"],
                "amount": expense["amount"],
            },
            request.user.expenses.filter(**get_localtime_kwargs(query_kwargs=True))
            .values("category__name")
            .annotate(amount=Sum("amount"))
            .order_by("category__name"),
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
            "expenses": expenses,
            "events": get_formatted_active_events(request.user),
            "transactions": transactions,
        },
    )
