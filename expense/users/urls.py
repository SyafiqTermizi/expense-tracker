from django.urls import path
from django.contrib.auth.views import LogoutView as SignOutView

from .views import SignInView, SignUpview, UpdateView

app_name = "users"

urlpatterns = [
    path("signin/", SignInView.as_view(), name="signin"),
    path("signout/", SignOutView.as_view(), name="signout"),
    path("signup/", SignUpview.as_view(), name="signup"),
    path("profile/", UpdateView.as_view(), name="profile"),
]
