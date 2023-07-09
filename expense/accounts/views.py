from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from .forms import AccountActionForm, AccountTransferForm, AccountForm
from .models import AccountAction, AccountBalance


@login_required
def transfer_view(request: HttpRequest) -> HttpResponse:
    user_accounts = request.user.accounts.values("name", "slug")

    if request.method == "GET":
        return render(
            request,
            "accounts/transfer.html",
            context={"accounts": user_accounts},
        )

    # Handle POST request
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


@login_required
def add_view(request: HttpRequest) -> HttpResponse:
    user_accounts = request.user.accounts.values("name", "slug")

    if request.method == "GET":
        return render(
            request,
            "accounts/add.html",
            context={"accounts": user_accounts},
        )

    # Handle POST request
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


@login_required
def detail_view(request: HttpRequest, slug: str) -> HttpResponse:
    account = get_object_or_404(
        request.user.accounts.all(),
        slug=slug,
    )

    account_actions = (
        request.user.account_actions.filter(
            account=account,
            created_at__month=timezone.now().month,
            created_at__year=timezone.now().year,
        )
        .order_by("-created_at")
        .select_related("expense", "account")
    )

    daily_balance = list(
        map(
            lambda balance: {
                "y": balance.amount,
                "x": balance.created_at.strftime("%d %b"),
            },
            request.user.account_balances.filter(
                created_at__month=timezone.now().month,
                created_at__year=timezone.now().year,
                action__account=account,
            )
            .order_by(
                "-created_at__day",
                "-created_at",
            )
            .distinct("created_at__day"),
        )
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

    try:
        available_balance = (
            request.user.account_balances.filter(
                action__account=account,
            )
            .latest()
            .amount
        )
    except AccountBalance.DoesNotExist:
        available_balance = 0

    return render(
        request,
        "accounts/detail.html",
        context={
            "account": account,
            "activities": activities,
            "balances": daily_balance,
            "available_balance": available_balance,
        },
    )


@login_required
def create_account_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, "accounts/create.html")

    form = AccountForm(user=request.user, data=request.POST)

    if form.is_valid():
        form.save()
        return redirect("dashboard:index")
    else:
        return render(
            request,
            "accounts/create.html",
            context={"form": form},
        )


@login_required
def delete_account_view(request: HttpRequest, slug: str) -> HttpResponse:
    account = get_object_or_404(
        request.user.accounts.all(),
        slug=slug,
    )

    if request.method == "POST":
        account.delete()
        return redirect("dashboard:index")

    return render(
        request,
        "accounts/delete.html",
        context={"account": account},
    )


@login_required
def update_account_view(request: HttpRequest, slug: str) -> HttpResponse:
    account = get_object_or_404(
        request.user.accounts.all(),
        slug=slug,
    )

    if request.method == "GET":
        return render(
            request,
            "accounts/update.html",
            context={
                "account": account,
                "form": AccountForm(user=request.user, instance=account),
            },
        )

    form = AccountForm(user=request.user, data=request.POST, instance=account)

    if form.is_valid():
        instance = form.save()
        return redirect("accounts:detail_view", slug=instance.slug)
    else:
        return render(
            request,
            "accounts/update.html",
            context={
                "account": account,
                "form": form,
            },
        )
