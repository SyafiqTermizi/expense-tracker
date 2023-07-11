from typing import Any, Dict, Optional
from django.contrib.auth import forms as base_forms
from django.forms import EmailField

from .models import User
from .tasks import send_email


class UserAdminChangeForm(base_forms.UserChangeForm):
    class Meta(base_forms.UserChangeForm.Meta):
        model = User
        field_classes = {"email": EmailField}


class UserAdminCreationForm(base_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(base_forms.UserCreationForm.Meta):
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}
        error_messages = {
            "email": {"unique": "This email has already been taken."},
        }


class UserCreationForm(base_forms.BaseUserCreationForm):
    class Meta(base_forms.BaseUserCreationForm.Meta):
        fields = ["email", "username", "currency"]
        model = User


class PasswordResetForm(base_forms.PasswordResetForm):
    def send_mail(
        self,
        subject_template_name: str,
        email_template_name: str,
        context: Dict[str, Any],
        from_email: str | None,
        to_email: str,
        html_email_template_name: str | None = None,
    ) -> None:
        return send_email(
            subject_template_name,
            email_template_name,
            context,
            from_email,
            to_email,
            html_email_template_name=html_email_template_name,
        )
