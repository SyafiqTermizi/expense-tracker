from django.contrib.auth.views import LoginView as BaseSignInView


class SignInView(BaseSignInView):
    template_name = "users/signin.html"
    redirect_authenticated_user = True
