from django.db.models import Sum

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone

from expense.accounts.models import AccountBalance, AccountAction
from expense.expenses.models import Expense


@login_required
def dashboard_view(request: HttpRequest) -> HttpResponse:
    """
    Returns an overview of the user's account balance and spending activities
    """

    # 1. Get account balance
    accounts = []
    for balance in (
        AccountBalance.objects.filter(belongs_to=request.user)
        .order_by(
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

    # 2. Get account activities for current month
    account_actions = (
        AccountAction.objects.filter(
            belongs_to=request.user,
            created_at__month=timezone.now().month,
            created_at__year=timezone.now().year,
        )
        .order_by("-created_at")
        .select_related("expense", "account")
    )

    activities = list(
        map(
            lambda acc_act: {
                "expense": hasattr(acc_act, "expense"),
                "account": str(acc_act.account),
                "created_at": acc_act.created_at.strftime("%d/%m/%Y"),
                "description": acc_act.description,
                "amount": acc_act.amount,
                "action": acc_act.action,
            },
            account_actions,
        )
    )

    # 3. Get expenses for current month
    expenses = list(
        map(
            lambda expense: {
                "category": expense["category__name"],
                "amount": expense["amount"],
            },
            Expense.objects.filter(
                belongs_to=request.user,
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
            "activities": activities,
            "expenses": expenses,
        },
    )
