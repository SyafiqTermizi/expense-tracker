from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max, Subquery
from django.db.models.functions import TruncDay
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import defaultfilters
from django.utils import timezone
from django.views.generic import DetailView

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


class MontlyAccountDetailView(LoginRequiredMixin, DetailView):
    def get_queryset(self):
        return self.request.user.accounts.all()

    def get_available_balance_context(self):
        try:
            return (
                self.request.user.account_balances.filter(
                    action__account=self.object,
                )
                .latest()
                .amount
            )
        except AccountBalance.DoesNotExist:
            return 0

    def get_daily_balance_context(self):
        last_daily_balance = (
            self.request.user.account_balances.filter(
                action__account=self.object,
                **self.month_year_db_kwargs,
            )
            .annotate(day=TruncDay("created_at"))
            .values("day")
            .annotate(the_date=Max("created_at"))
            .values_list("the_date", flat=True)
        )

        return list(
            map(
                lambda bal: {
                    "y": bal.amount,
                    "x": defaultfilters.date(bal.date, "d M"),
                },
                self.request.user.account_balances.filter(
                    action__account=self.object,
                    created_at__in=Subquery(last_daily_balance),
                )
                .annotate(date=TruncDay("created_at"))
                .order_by("created_at"),
            )
        )

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.set_month_year_kwargs()

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return {
            "account": self.object,
            "transactions": get_transactions_with_expense_data(
                user=self.request.user,
                account=self.object,
                **self.month_year_kwargs,
            ),
            "balances": self.get_daily_balance_context(),
            "available_balance": self.get_available_balance_context(),
            "month_name": self.month_name,
        }

    def set_month_year_kwargs(self):
        self.month_year_db_kwargs = get_localtime_kwargs(query_kwargs=True)
        self.month_year_kwargs = get_localtime_kwargs()

        form = MonthQueryParamForm(data=self.request.GET)

        if form.is_valid():
            self.month_year_kwargs.update(
                {
                    "month": form.cleaned_data["month"],
                    "year": form.cleaned_data["year"],
                }
            )
            self.month_year_db_kwargs.update(
                {
                    "created_at__month": form.cleaned_data["month"],
                    "created_at__year": form.cleaned_data["year"],
                }
            )

        self.month_name = form.get_month_name() or timezone.localtime(
            timezone.now()
        ).strftime("%B")


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
