from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import View

from expense.accounts.utils import get_latest_account_balance
from expense.events.models import Event
from expense.utils import MonthQueryParamForm, get_localtime_kwargs

from ..forms import AddExpenseForm, ExpenseImageForm, UpdateExpenseForm
from ..utils import get_formatted_user_expense_for_month


@login_required
def add_expense_view(request: HttpRequest) -> HttpResponse:
    user_accounts = get_latest_account_balance(request.user)
    expense_categories = request.user.expense_categories.values("name", "slug")
    active_events = Event.objects.get_user_active_events(request.user).values(
        "name",
        "slug",
    )

    if request.method == "GET":
        selected_account = request.GET.get("account", None)

        for account in user_accounts:
            if account["slug"] == selected_account:
                account.update({"selected": True})

        return render(
            request,
            "expenses/add_expense.html",
            context={
                "accounts": user_accounts,
                "active_events": active_events,
                "categories": expense_categories,
            },
        )

    form = AddExpenseForm(user=request.user, data=request.POST, files=request.FILES)

    if not form.is_valid():
        return render(
            request,
            "expenses/add_expense.html",
            context={
                "form": form,
                "accounts": user_accounts,
                "categories": expense_categories,
            },
            status=400,
        )

    form.save()

    return redirect("dashboard:index")


def update_expense_view(request: HttpRequest, slug: str) -> HttpResponse:
    expense = (
        request.user.expenses.filter(slug=slug)
        .select_related("from_action__account", "category")
        .first()
    )
    expense_categories = request.user.expense_categories.values("name", "slug")

    if request.method == "GET":
        return render(
            request=request,
            template_name="expenses/update_expense.html",
            context={
                "expense": expense,
                "categories": expense_categories,
                "image": expense.images.first(),
                "expense_form": UpdateExpenseForm(
                    user=request.user,
                    instance=expense,
                ),
            },
        )

    expense_form = UpdateExpenseForm(
        user=request.user,
        instance=expense,
        data=request.POST,
    )
    image_form = ExpenseImageForm(
        request.POST,
        request.FILES,
        instance=expense.images.first(),
    )

    if not expense_form.is_valid() or not image_form.is_valid():
        return render(
            request,
            template_name="expenses/update_expense.html",
            context={
                "expense": expense,
                "expense_form": expense_form,
                "image_form": image_form,
                "categories": expense_categories,
            },
            status=400,
        )

    expense = expense_form.save()
    expense.from_action.description = expense.description
    expense.from_action.save()

    image_form.save(expense=expense)

    return redirect("dashboard:index")


class MonthlyExpenseDetailView(LoginRequiredMixin, View):
    def get_expense_by_category_context(self):
        expense_by_category = {}
        for category_expense in (
            self.request.user.expenses.filter(**self.month_year_kwargs)
            .values("category__name")
            .annotate(total=Sum("amount"))
        ):
            expense_by_category.update(
                {category_expense["category__name"]: category_expense["total"]}
            )

        return expense_by_category

    def expense_by_account_context(self):
        expense_by_account = {}
        for account_expense in (
            self.request.user.expenses.filter(**self.month_year_kwargs)
            .values("from_action__account__name")
            .annotate(total=Sum("amount"))
        ):
            expense_by_account.update(
                {
                    account_expense["from_action__account__name"]: account_expense[
                        "total"
                    ]
                }
            )
        return expense_by_account

    def get_expense_this_month_context(self):
        return get_formatted_user_expense_for_month(
            self.request.user.expenses.filter(
                belongs_to=self.request.user,
                **self.month_year_kwargs,
            )
            .order_by("-created_at")
            .values(
                "slug",
                "from_action__account__name",
                "created_at",
                "description",
                "amount",
                "category__name",
            )
        )

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.set_month_year_kwargs()

        context = self.get_context_data()
        return render(request, "expenses/detail.html", context=context)

    def get_all_expense_months_context(self):
        return (
            self.request.user.expenses.annotate(date=TruncMonth("created_at"))
            .distinct("date")
            .values("date")
        )

    def get_context_data(self, **kwargs):
        expense_this_month = self.get_expense_this_month_context()
        total_expense = sum(expense["amount"] for expense in expense_this_month)

        return {
            "expense_by_category": self.get_expense_by_category_context(),
            "expense_by_account": self.expense_by_account_context(),
            "expenses": expense_this_month,
            "total_expense": total_expense,
            "all_expense_months": self.get_all_expense_months_context(),
            "month_name": self.month_name,
        }

    def set_month_year_kwargs(self):
        self.month_year_kwargs = get_localtime_kwargs(query_kwargs=True)

        form = MonthQueryParamForm(data=self.request.GET)
        if form.is_valid():
            self.month_year_kwargs.update(
                {
                    "created_at__month": form.cleaned_data["month"],
                    "created_at__year": form.cleaned_data["year"],
                }
            )

        self.month_name = form.get_month_name() or timezone.localtime(
            timezone.now()
        ).strftime("%B")


@login_required
def expense_detail_api_view(request: HttpResponse, slug: str) -> JsonResponse:
    expense = (
        request.user.expenses.filter(slug=slug)
        .select_related("category", "from_action__account")
        .first()
    )

    images = []
    for image in expense.images.all():
        images.append(image.image.url)

    res = {
        "account": expense.from_action.account.name,
        "description": expense.description,
        "category": expense.category.name,
        "amount": expense.amount,
        "created_at": expense.created_at,
        "images": images,
        "url": expense.get_absolute_url(),
    }
    return JsonResponse(data=res)
