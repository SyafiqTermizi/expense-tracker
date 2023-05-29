from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone

from expense.accounts.models import Account, AccountAction


@login_required
def dashboard_view(request: HttpRequest) -> HttpResponse:
    """
    Returns an overview of the user's account balance and spending activities
    """

    # 1. Get account balance
    account_balance = {}
    for balance in (
        Account.objects.order_by(
            "action__account_type__type",
            "-created_at",
        )
        .distinct("action__account_type__type")
        .values("amount", "action__account_type__type")
    ):
        account_balance[balance["action__account_type__type"]] = balance["amount"]

    # 2. Get account activities
    account_actions = (
        AccountAction.objects.filter(
            belongs_to=request.user,
            created_at__gte=(timezone.now() - timedelta(days=30)),
        )
        .order_by("-created_at")
        .select_related("expense", "account_type")
    )

    activities = list(
        map(
            lambda acc_act: {
                "expense": hasattr(acc_act, "expense"),
                "account_type": str(acc_act.account_type),
                "created_at": acc_act.created_at.strftime("%d-%m-%Y"),
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
