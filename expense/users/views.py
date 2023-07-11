from typing import Any, Dict
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView as BaseSignInView,
    PasswordResetView as BasePasswordResetView,
    PasswordResetConfirmView as BasePasswordResetConfirmView,
    PasswordResetDoneView as BasePasswordResetDoneView,
    PasswordResetCompleteView as BasePasswordResetCompleteView,
)
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView

from .forms import UserCreationForm, PasswordResetForm
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

    def get_context_data(sAelf, **kwargs: Any) -> Dict[str, Any]:
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


class PasswordResetView(BasePasswordResetView):
    template_name = "users/password_reset.html"
    email_template_name = "users/email/password_reset.html"
    html_email_template_name = "users/email/password_reset_html.html"
    success_url = reverse_lazy("users:password_reset_done")
    form_class = PasswordResetForm


class PasswordResetConfirmView(BasePasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")

    def form_valid(self, form: Any) -> HttpResponse:
        print("shit valid")
        return super().form_valid(form)

    def form_invalid(self, form: Any) -> HttpResponse:
        print("shit invalid")
        return super().form_invalid(form)


class PasswordResetDoneView(BasePasswordResetDoneView):
    template_name = "users/password_reset_done.html"


class PasswordResetCompleteView(BasePasswordResetCompleteView):
    template_name = "users/password_reset_complete.html"
