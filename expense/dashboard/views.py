from django.db.models import Sum

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone

from expense.accounts.utils import get_actions_with_expense_data


@login_required
def dashboard_view(request: HttpRequest) -> HttpResponse:
    """
    Returns an overview of the user's account balance and spending activities
    """

    # 1. Get account balance
    accounts = []
    for balance in (
        request.user.account_balances.order_by(
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
            }
        )

    # 1.1 Add accounts with no balance
    for account in request.user.accounts.exclude(
        name__in=list(map(lambda acc: acc["name"], accounts))
    ):
        accounts.append(
            {
                "name": account.name,
                "balance": 0,
                "url": account.get_absolute_url(),
            }
        )

    # 3. Get expenses for current month
    expenses = list(
        map(
            lambda expense: {
                "category": expense["category__name"],
                "amount": expense["amount"],
            },
            request.user.expenses.filter(
                created_at__month=timezone.now().month,
                created_at__year=timezone.now().year,
            )
            .values("category__name")
            .annotate(amount=Sum("amount")),
        )
    )

    return render(
        request,
        "dashboard/dashboard.html",
        context={
            "accounts": accounts,
            "activities": get_actions_with_expense_data(
                request.user,
                timezone.now().month,
                timezone.now().year,
                account=None,
            ),
            "expenses": expenses,
        },
    )
