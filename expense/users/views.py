from typing import Any, Dict
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseSignInView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import FormView, UpdateView

from .forms import UserCreationForm
from .models import CURRENCIES, User


class CurrencyContextMixin:
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({"currencies": CURRENCIES})
        return context


class SignInView(BaseSignInView):
    template_name = "users/signin.html"
    redirect_authenticated_user = True


class SignUpview(CurrencyContextMixin, FormView):
    template_name = "users/signup.html"
    form_class = UserCreationForm

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({"currencies": CURRENCIES})
        return context

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        login(self.request, form.save())
        return redirect("dashboard:index")


class UpdateView(LoginRequiredMixin, CurrencyContextMixin, UpdateView):
    model = User
    fields = ["username", "email", "currency"]
    template_name = "users/profile.html"

    def get_object(self, *args, **kwargs):
        return get_object_or_404(User, pk=self.request.user.pk)
