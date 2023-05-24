from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from expense.accounts.models import Account, AccountAction


@login_required
def dashboard_view(request: HttpRequest) -> HttpResponse:
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

    activities = AccountAction.objects.filter(belongs_to=request.user).order_by(
        "-created_at"
    )[:30]

    return render(
        request,
        "dashboard/dashboard.html",
        context={
            "balance": account_balance,
            "activities": activities,
        },
    )
