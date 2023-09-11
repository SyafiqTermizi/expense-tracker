from typing import Any, Dict, List

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max, Subquery
from django.db.models.functions import TruncDay
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.template import defaultfilters
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    UpdateView,
)

from expense.accounts.utils import (
    get_latest_account_balance,
    get_transactions_with_expense_data,
)
from expense.utils import MonthQueryParamForm, get_localtime_kwargs

from .forms import AccountActionForm, AccountForm, AccountTransferForm
from .models import Account, AccountAction, AccountBalance


class TransferView(LoginRequiredMixin, FormView):
    form_class = AccountTransferForm
    template_name = "accounts/transfer.html"
    success_url = reverse_lazy("dashboard:index")

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "accounts": get_latest_account_balance(self.request.user),
        }

    def get_form_kwargs(self) -> Dict[str, Any]:
        return {"user": self.request.user, **super().get_form_kwargs()}

    def form_valid(self, form: Any) -> HttpResponse:
        form.save()
        return super().form_valid(form)


@login_required
def add_view(request: HttpRequest) -> HttpResponse:
    """Add money into an account"""

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
            status=400,
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
            "all_account_balance_month": self.request.user.account_balances.dates(
                "created_at", "month"
            ),
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


class CreateAccountView(LoginRequiredMixin, CreateView):
    form_class = AccountForm
    model = Account
    success_url = reverse_lazy("dashboard:index")

    def get_form_kwargs(self) -> Dict[str, Any]:
        return {"user": self.request.user, **super().get_form_kwargs()}


class DeleteAccountView(LoginRequiredMixin, DeleteView):
    model = Account
    success_url = reverse_lazy("dashboard:index")

    def get_queryset(self):
        return self.request.user.accounts.all()


class UpdateAccountView(LoginRequiredMixin, UpdateView):
    form_class = AccountForm
    model = Account

    def get_form_kwargs(self) -> Dict[str, Any]:
        return {"user": self.request.user, **super().get_form_kwargs()}

    def get_queryset(self):
        return self.request.user.accounts.all()

    def get_success_url(self) -> str:
        return reverse("accounts:detail_view", kwargs={"slug": self.object.slug})

    def get_template_names(self) -> List[str]:
        return super().get_template_names()
