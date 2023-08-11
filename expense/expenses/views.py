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
    AddExpenseImageForm,
    CategoryForm,
    MonthQueryParamForm,
)
from .utils import get_formatted_user_expense_for_month


@login_required
def add_expense_view(request: HttpRequest) -> HttpResponse:
    user_accounts = get_latest_account_balance(request.user)
    expense_categories = request.user.expense_categories.values("name", "slug")

    # Return early if rqeuest is GET
    if request.method == "GET":
        return render(
            request,
            "expenses/add_expense.html",
            context={
                "accounts": user_accounts,
                "categories": expense_categories,
            },
        )

    form_error = False

    # validate expense form
    expense_form = AddExpenseForm(user=request.user, data=request.POST)
    if expense_form.is_valid():
        expense = expense_form.save()
    else:
        form_error = True

    # validate image form
    if request.FILES:
        image_form = AddExpenseImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            image_instance = image_form.save(commit=False)
            image_instance.expense = expense
            image_instance.save()
        else:
            form_error = True

    # render form with errors
    if form_error:
        return render(
            request,
            "expenses/add_expense.html",
            context={
                "expense_form": expense_form,
                "image_form": image_form,
                "accounts": user_accounts,
                "categories": expense_categories,
            },
        )

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
        "created_at__month": timezone.now().month,
        "created_at__year": timezone.now().year,
    }

    form = MonthQueryParamForm(data=request.GET)
    if form.is_valid():
        filter_kwargs.update(
            {
                "created_at__month": form.cleaned_data["month"],
                "created_at__year": form.cleaned_data["year"],
            }
        )

    expense_by_category = list(
        map(
            lambda x: {"x": x["category__name"], "y": x["total"]},
            (
                request.user.expenses.filter(**filter_kwargs)
                .values("category__name")
                .annotate(total=Sum("amount"))
            ),
        )
    )

    expense_by_account = list(
        map(
            lambda x: {"x": x["from_action__account__name"], "y": x["total"]},
            (
                request.user.expenses.filter(**filter_kwargs)
                .values("from_action__account__name")
                .annotate(total=Sum("amount"))
            ),
        )
    )

    expense_this_month = get_formatted_user_expense_for_month(
        request.user.expenses.filter(belongs_to=request.user, **filter_kwargs)
        .order_by("-created_at")
        .values(
            "pk",
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

    month_int = form.cleaned_data["month"] if form.is_valid() else timezone.now().month
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
def expense_detail_api_view(request: HttpResponse, pk: int) -> JsonResponse:
    expense = (
        request.user.expenses.filter(pk=pk)
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
    }
    return JsonResponse(data=res)
