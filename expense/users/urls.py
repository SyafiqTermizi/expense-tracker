from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import SignInView

app_name = "users"

urlpatterns = [
    path("signin/", SignInView.as_view(), name="signin"),
    path("signout/", LogoutView.as_view(), name="signout"),
]
