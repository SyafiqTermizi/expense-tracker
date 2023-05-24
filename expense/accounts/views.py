from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import AccountActionForm, AccountTransferForm, WithdrawForm
from .models import AccountType, Account, AccountAction


@login_required
def dashboard_view(request: HttpRequest) -> HttpResponse:
    accounts = {}
    for balance in (
        Account.objects.order_by("action__account_type__type", "-created_at")
        .distinct("action__account_type__type")
        .values("amount", "action__account_type__type")
    ):
        accounts[balance["action__account_type__type"]] = balance["amount"]

    actions = AccountAction.objects.filter(belongs_to=request.user).order_by(
        "-created_at"
    )[:30]

    return render(
        request,
        "accounts/dashboard.html",
        context={
            "accounts": accounts,
            "actions": actions,
        },
    )


@login_required
def transfer_view(request: HttpRequest) -> HttpResponse:
    user_accounts = request.user.account_types.all()

    if request.method == "POST":
        form = AccountTransferForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            return redirect("dashboard:index")
        else:
            return render(
                request,
                "accounts/transfer.html",
                context={
                    "form": form,
                    "accounts": user_accounts,
                },
            )

    return render(
        request,
        "accounts/transfer.html",
        context={"accounts": user_accounts},
    )


@login_required
def add_view(request: HttpRequest) -> HttpResponse:
    user_accounts = request.user.account_types.all()

    if request.method == "POST":
        form = AccountActionForm(
            data={
                **request.POST.dict(),
                "belongs_to": request.user,
                "action": AccountAction.Action.CREDIT,
            }
        )

        if form.is_valid():
            form.save(commit=True)
            return redirect("dashboard:index")
        else:
            return render(
                request,
                "accounts/add.html",
                context={
                    "form": form,
                    "accounts": user_accounts,
                },
            )

    return render(
        request,
        "accounts/add.html",
        context={"accounts": user_accounts},
    )


@login_required
def withdraw_view(request: HttpRequest) -> HttpResponse:
    user_accounts = request.user.account_types.exclude(type=AccountType.Type.CASH)
    if request.method == "POST":
        form = WithdrawForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard:index")
        else:
            return render(
                request,
                "accounts/withdraw.html",
                context={
                    "form": form,
                    "accounts": user_accounts,
                },
            )
    return render(
        request,
        "accounts/withdraw.html",
        context={"accounts": user_accounts},
    )
