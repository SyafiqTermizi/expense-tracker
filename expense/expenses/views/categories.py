from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from ..forms import CategoryForm


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
