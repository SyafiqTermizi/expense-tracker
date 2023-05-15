from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import AccountTransferForm
from .models import AccountType, Account, AccountAction


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

    actions = AccountAction.objects.filter(belongs_to=request.user).order_by(
        "-created_at"
    )[:30]

    return render(
        request,
        "accounts/dashboard.html",
        context={
            "accounts": {
                "income": latest_income,
                "saving": latest_saving,
            },
            "actions": actions,
        },
    )


@login_required
def transfer_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = AccountTransferForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            return redirect("accounts:dashboard_view")

    user_accounts = request.user.account_types.all()
    return render(
        request,
        "accounts/transfer.html",
        context={
            "form": AccountTransferForm(user=request.user),
            "accounts": user_accounts,
        },
    )
