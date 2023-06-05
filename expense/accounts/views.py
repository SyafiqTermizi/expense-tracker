from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from .forms import AccountActionForm, AccountTransferForm
from .models import AccountAction, Account


@login_required
def transfer_view(request: HttpRequest) -> HttpResponse:
    user_accounts = request.user.accounts.values("name", "slug")

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
    user_accounts = request.user.accounts.values("name", "slug")

    if request.method == "POST":
        form = AccountActionForm(
            user=request.user,
            data={
                **request.POST.dict(),
                "belongs_to": request.user,
                "action": AccountAction.Action.CREDIT,
            },
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
def detail_view(request: HttpRequest, slug: str) -> HttpResponse:
    account = get_object_or_404(
        Account.objects.filter(belongs_to=request.user),
        slug=slug,
    )

    account_actions = (
        AccountAction.objects.filter(
            account=account,
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
        "accounts/detail.html",
        context={
            "account": account,
            "activities": activities,
        },
    )
