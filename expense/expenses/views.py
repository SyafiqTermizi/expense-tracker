from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AddExpenseForm, CategoryForm


@login_required
def add_expense_view(request: HttpRequest) -> HttpResponse:
    user_accounts = request.user.accounts.values("name", "slug")
    expense_categories = request.user.expense_categories.all()

    if request.method == "POST":
        form = AddExpenseForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            return redirect("dashboard:index")
        else:
            return render(
                request,
                "expenses/add_expense.html",
                context={
                    "form": form,
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
        context={"categories": request.user.expense_categories.values("name", "pk")},
    )


@login_required
def update_expense_categories(request: HttpRequest, pk: int) -> HttpResponse:
    category = get_object_or_404(request.user.expense_categories, pk=pk)

    if request.method == "POST":
        form = CategoryForm(data=request.POST, instance=category)

        if form.is_valid():
            category = form.save(commit=False)
            category.belongs_to = request.user
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
def delete_expense_categories(request: HttpRequest, pk: int) -> HttpResponse:
    category = get_object_or_404(request.user.expense_categories, pk=pk)

    if request.method == "POST":
        category.delete()
        return redirect("expenses:categories:list")

    return render(
        request,
        "expenses/delete_category.html",
        context={"category": category},
    )
