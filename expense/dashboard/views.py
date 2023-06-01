from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone

from expense.accounts.models import AccountBalance, AccountAction


@login_required
def dashboard_view(request: HttpRequest) -> HttpResponse:
    """
    Returns an overview of the user's account balance and spending activities
    """

    # 1. Get account balance
    account_balance = {}
    for balance in (
        AccountBalance.objects.order_by(
            "action__account__name",
            "-created_at",
        )
        .distinct("action__account__name")
        .values("amount", "action__account__name")
    ):
        account_balance[balance["action__account__name"]] = balance["amount"]

    # 2. Get account activities
    account_actions = (
        AccountAction.objects.filter(
            belongs_to=request.user,
            created_at__gte=(timezone.now() - timedelta(days=30)),
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

    return render(
        request,
        "dashboard/dashboard.html",
        context={"balance": account_balance, "activities": activities},
    )
