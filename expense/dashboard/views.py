from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone

from expense.accounts.models import Account, AccountAction

from .serializers import AccountActionAndExpenseSerializer


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

    return render(
        request,
        "dashboard/dashboard.html",
        context={
            "balance": account_balance,
            "activities": AccountActionAndExpenseSerializer(
                AccountAction.objects.filter(
                    belongs_to=request.user,
                    created_at__gte=(timezone.now() - timedelta(days=30)),
                )
                .order_by("-created_at")
                .select_related("expense"),
                many=True,
            ).data,
        },
    )
