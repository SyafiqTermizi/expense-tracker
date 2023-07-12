from django.db.models import Sum

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone

from expense.accounts.utils import (
    get_actions_with_expense_data,
    get_latest_account_balance,
)


@login_required
def dashboard_view(request: HttpRequest) -> HttpResponse:
    """
    Returns an overview of the user's account balance and spendings
    """

    # 2. Get expenses for current month
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
            "accounts": get_latest_account_balance(request.user),
            "transactions": get_actions_with_expense_data(
                request.user,
                timezone.now().month,
                timezone.now().year,
                account=None,
            ),
            "expenses": expenses,
        },
    )
