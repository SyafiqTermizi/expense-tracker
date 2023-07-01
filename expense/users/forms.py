from django.contrib.auth import forms as base_forms
from django.forms import EmailField

from .models import User


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
        fields = ["email", "username"]
        model = User
