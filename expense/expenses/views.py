from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

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
            return render(request, "expenses/add_category.html", context={"form": form})
    return render(request, "expenses/add_category.html")
