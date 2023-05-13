from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import AccountType, Account


@login_required
def dashboard_view(request: HttpRequest) -> HttpResponse:
    try:
        income_account = Account.objects.filter(
            belongs_to=request.user,
            action__account_type__type__in=[AccountType.Type.INCOME],
        ).latest()
    except Account.DoesNotExist:
        latest_income = 0
    else:
        latest_income = income_account.amount

    try:
        saving_account = Account.objects.filter(
            belongs_to=request.user,
            action__account_type__type__in=[AccountType.Type.SAVING],
        ).latest()
    except Account.DoesNotExist:
        latest_saving = 0
    else:
        latest_saving = saving_account.amount

    return render(
        request,
        "accounts/dashboard.html",
        context={
            "accounts": {
                "income": latest_income,
                "saving": latest_saving,
            }
        },
    )
