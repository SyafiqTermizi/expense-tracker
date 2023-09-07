from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from ..forms import CategoryForm
from ..models import Category


class CreateCategoryView(LoginRequiredMixin, CreateView):
    form_class = CategoryForm
    model = Category

    def get_form_kwargs(self):
        return {"user": self.request.user, **super().get_form_kwargs()}

    def get_queryset(self):
        return self.request.user.expense_categories.all()

    def get_success_url(self) -> str:
        return self.request.GET.get("next") or reverse("dashboard:index")


class DeleteCategoryView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy("expenses:categories:list")

    def get_queryset(self):
        return self.request.user.expense_categories.all()


class ListCategoryView(LoginRequiredMixin, ListView):
    model = Category

    def get_context_data(self, **kwargs):
        return {
            "categories": self.request.user.expense_categories.values("name", "slug")
        }


class UpdateCategoryView(LoginRequiredMixin, UpdateView):
    form_class = CategoryForm
    model = Category

    def get_form_kwargs(self):
        return {"user": self.request.user, **super().get_form_kwargs()}

    def get_queryset(self):
        return self.request.user.expense_categories.all()

    def get_success_url(self) -> str:
        return self.request.GET.get("next") or reverse("expenses:categories:list")
