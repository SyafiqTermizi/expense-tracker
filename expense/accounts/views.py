from django.db.models import Max, Subquery
from django.db.models.functions import TruncDay
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template import defaultfilters
from django.utils import timezone

from expense.accounts.utils import (
    get_actions_with_expense_data,
    get_latest_account_balance,
)

from .forms import AccountActionForm, AccountTransferForm, AccountForm
from .models import AccountAction, AccountBalance


@login_required
def transfer_view(request: HttpRequest) -> HttpResponse:
    user_accounts = get_latest_account_balance(request.user)

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
    user_accounts = get_latest_account_balance(request.user)

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

    last_daily_transcation = (
        request.user.account_balances.filter(
            action__account=account,
            created_at__month=timezone.now().month,
            created_at__year=timezone.now().year,
        )
        .annotate(day=TruncDay("created_at"))
        .values("day")
        .annotate(the_date=Max("created_at"))
        .values_list("the_date", flat=True)
    )

    daily_balance = list(
        map(
            lambda bal: {
                "y": bal.amount,
                "x": defaultfilters.date(bal.date, "d M"),
            },
            request.user.account_balances.filter(
                action__account=account,
                created_at__in=Subquery(last_daily_transcation),
            )
            .annotate(date=TruncDay("created_at"))
            .order_by("created_at"),
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
            "transactions": get_actions_with_expense_data(
                request.user,
                timezone.now().month,
                timezone.now().year,
                account=account,
            ),
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
