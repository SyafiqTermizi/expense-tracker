import calendar

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.text import slugify

from expense.accounts.utils import get_latest_account_balance

from .forms import (
    AddExpenseForm,
    ExpenseImageForm,
    CategoryForm,
    MonthQueryParamForm,
    UpdateExpenseForm,
)
from .utils import get_formatted_user_expense_for_month


@login_required
def add_expense_view(request: HttpRequest) -> HttpResponse:
    user_accounts = get_latest_account_balance(request.user)
    expense_categories = request.user.expense_categories.values("name", "slug")

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
                "categories": expense_categories,
            },
        )

    expense_form = AddExpenseForm(user=request.user, data=request.POST)

    if not request.FILES:
        if expense_form.is_valid():
            expense = expense_form.save()
            return redirect("dashboard:index")
        return render(
            request,
            "expenses/add_expense.html",
            context={
                "expense_form": expense_form,
                "accounts": user_accounts,
                "categories": expense_categories,
            },
        )

    image_form = ExpenseImageForm(request.POST, request.FILES)

    if not expense_form.is_valid() or not image_form.is_valid():
        return render(
            request,
            "expenses/add_expense.html",
            context={
                "expense_form": expense_form,
                "image_form": image_form if request.FILES else None,
                "accounts": user_accounts,
                "categories": expense_categories,
            },
        )

    expense = expense_form.save()
    image_form.save(expense=expense)

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

    if not request.FILES:
        if expense_form.is_valid():
            expense = expense_form.save()
            expense.from_action.description = expense.description
            expense.from_action.save()
            return redirect("dashboard:index")
        return render(
            request,
            "expenses/add_expense.html",
            context={
                "expense_form": expense_form,
                "categories": expense_categories,
            },
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
                "categories": expense_categories,
            },
        )

    expense = expense_form.save()
    expense.from_action.description = expense.description
    expense.from_action.save()

    image_form.save(expense=expense)

    return redirect("dashboard:index")


@login_required
def add_expense_category(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, "expenses/category_form.html")

    form = CategoryForm(data=request.POST)

    if form.is_valid():
        category = form.save(commit=False)
        category.belongs_to = request.user
        category.slug = slugify(category.name)
        category.save()
        return redirect(
            request.GET.get(
                "next",
                "dashboard:index",
            )
        )
    else:
        return render(request, "expenses/category_form.html", context={"form": form})


@login_required
def list_expense_categories(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "expenses/list_category.html",
        context={"categories": request.user.expense_categories.values("name", "slug")},
    )


@login_required
def update_expense_categories(request: HttpRequest, slug: str) -> HttpResponse:
    category = get_object_or_404(request.user.expense_categories, slug=slug)

    if request.method == "GET":
        return render(
            request,
            "expenses/category_form.html",
            context={"form": CategoryForm(instance=category)},
        )

    form = CategoryForm(data=request.POST, instance=category)

    if form.is_valid():
        category = form.save(commit=False)
        category.belongs_to = request.user
        category.slug = slugify(category.name)
        category.save()
        return redirect(
            request.GET.get(
                "next",
                "dashboard:index",
            )
        )
    else:
        return render(request, "expenses/category_form.html", context={"form": form})


@login_required
def delete_expense_categories(request: HttpRequest, slug: str) -> HttpResponse:
    category = get_object_or_404(request.user.expense_categories, slug=slug)

    if request.method == "POST":
        category.delete()
        return redirect("expenses:categories:list")

    return render(
        request,
        "expenses/delete_category.html",
        context={"category": category},
    )


@login_required
def monthly_expense_detail_view(request: HttpRequest) -> HttpResponse:
    filter_kwargs = {
        "created_at__month": timezone.localtime(timezone.now()).month,
        "created_at__year": timezone.localtime(timezone.now()).year,
    }

    form = MonthQueryParamForm(data=request.GET)
    if form.is_valid():
        filter_kwargs.update(
            {
                "created_at__month": form.cleaned_data["month"],
                "created_at__year": form.cleaned_data["year"],
            }
        )

    expense_by_category = {}
    for category_expense in (
        request.user.expenses.filter(**filter_kwargs)
        .values("category__name")
        .annotate(total=Sum("amount"))
    ):
        expense_by_category.update(
            {category_expense["category__name"]: category_expense["total"]}
        )

    expense_by_account = {}
    for account_expense in (
        request.user.expenses.filter(**filter_kwargs)
        .values("from_action__account__name")
        .annotate(total=Sum("amount"))
    ):
        expense_by_account.update(
            {account_expense["from_action__account__name"]: account_expense["total"]}
        )

    expense_this_month = get_formatted_user_expense_for_month(
        request.user.expenses.filter(belongs_to=request.user, **filter_kwargs)
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

    all_expense_months = (
        request.user.expenses.annotate(date=TruncMonth("created_at"))
        .distinct("date")
        .values("date")
    )

    total_expense = sum(expense["amount"] for expense in expense_this_month)

    month_int = (
        form.cleaned_data["month"]
        if form.is_valid()
        else timezone.localtime(timezone.now()).month
    )
    month_name = calendar.month_name[month_int]

    return render(
        request,
        "expenses/detail.html",
        context={
            "expense_by_category": expense_by_category,
            "expense_by_account": expense_by_account,
            "expenses": expense_this_month,
            "total_expense": total_expense,
            "all_expense_months": all_expense_months,
            "month_name": month_name,
        },
    )


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
