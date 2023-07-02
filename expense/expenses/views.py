from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.text import slugify

from .forms import AddExpenseForm, AddExpenseImageForm, CategoryForm


@login_required
def add_expense_view(request: HttpRequest) -> HttpResponse:
    user_accounts = request.user.accounts.values("name", "slug")
    expense_categories = request.user.expense_categories.values("name", "slug")

    if request.method == "POST":
        expense_form = AddExpenseForm(user=request.user, data=request.POST)
        image_form = AddExpenseImageForm(request.POST, request.FILES)

        if expense_form.is_valid() and image_form.is_valid():
            expense = expense_form.save()
            image_instance = image_form.save(commit=False)
            image_instance.expense = expense
            image_instance.save()
            return redirect("dashboard:index")
        else:
            return render(
                request,
                "expenses/add_expense.html",
                context={
                    "form": expense_form,
                    "accounts": user_accounts,
                    "categories": expense_categories,
                },
            )

    return render(
        request,
        "expenses/add_expense.html",
        context={
            "accounts": user_accounts,
            "categories": expense_categories,
        },
    )


@login_required
def add_expense_category(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
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
            return render(
                request, "expenses/category_form.html", context={"form": form}
            )
    return render(request, "expenses/category_form.html")


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

    if request.method == "POST":
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
            return render(
                request, "expenses/category_form.html", context={"form": form}
            )
    return render(
        request,
        "expenses/category_form.html",
        context={"form": CategoryForm(instance=category)},
    )


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
def expense_detail_view(request: HttpRequest) -> HttpResponse:
    expense_by_category = list(
        map(
            lambda x: {"x": x["category__name"], "y": x["total"]},
            (
                request.user.expenses.filter(
                    created_at__month=timezone.now().month,
                    created_at__year=timezone.now().year,
                )
                .values("category__name")
                .annotate(total=Sum("amount"))
            ),
        )
    )

    expense_by_account = list(
        map(
            lambda x: {"x": x["from_action__account__name"], "y": x["total"]},
            (
                request.user.expenses.filter(
                    created_at__month=timezone.now().month,
                    created_at__year=timezone.now().year,
                )
                .values("from_action__account__name")
                .annotate(total=Sum("amount"))
            ),
        )
    )

    expense_this_month = request.user.expenses.filter(
        created_at__month=timezone.now().month,
        created_at__year=timezone.now().year,
    ).values("from_action__account__name", "created_at", "description", "amount")

    return render(
        request,
        "expenses/detail.html",
        context={
            "expense_by_category": expense_by_category,
            "expense_by_account": expense_by_account,
            "expenses": expense_this_month,
        },
    )
