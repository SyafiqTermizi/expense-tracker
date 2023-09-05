from django.contrib.auth.decorators import login_required
from django.db.models import Max, Subquery
from django.db.models.functions import TruncDay
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import defaultfilters
from django.utils import timezone

from expense.accounts.utils import (
    get_latest_account_balance,
    get_transactions_with_expense_data,
)
from expense.utils import MonthQueryParamForm, get_localtime_kwargs

from .forms import AccountActionForm, AccountForm, AccountTransferForm
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
        selected_account = request.GET.get("account", None)

        for account in user_accounts:
            if account["slug"] == selected_account:
                account.update({"selected": True})

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

    month_year_db_kwargs = get_localtime_kwargs(query_kwargs=True)
    month_year_kwargs = get_localtime_kwargs()
    form = MonthQueryParamForm(data=request.GET)
    if form.is_valid():
        month_year_kwargs.update(
            {
                "month": form.cleaned_data["month"],
                "year": form.cleaned_data["year"],
            }
        )
        month_year_db_kwargs.update(
            {
                "created_at__month": form.cleaned_data["month"],
                "created_at__year": form.cleaned_data["year"],
            }
        )

    last_daily_transcation = (
        request.user.account_balances.filter(
            action__account=account,
            **month_year_db_kwargs,
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

    return render(
        request,
        "accounts/detail.html",
        context={
            "account": account,
            "transactions": get_transactions_with_expense_data(
                user=request.user,
                account=account,
                **month_year_kwargs,
            ),
            "balances": daily_balance,
            "available_balance": available_balance,
            "month_name": form.get_month_name()
            or timezone.localtime(timezone.now()).strftime("%B"),
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
