from typing import Any, Dict
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as BaseSignInView
from django.shortcuts import redirect
from django.views.generic import FormView

from .forms import UserCreationForm
from .models import CURRENCIES


class SignInView(BaseSignInView):
    template_name = "users/signin.html"
    redirect_authenticated_user = True


class SignUpview(FormView):
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
