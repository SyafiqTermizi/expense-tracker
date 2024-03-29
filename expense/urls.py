"""
URL configuration for expense project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urls = [
    path("", include("expense.dashboard.urls")),
    path("accounts/", include("expense.accounts.urls")),
    path("expenses/", include("expense.expenses.urls")),
    path("users/", include("expense.users.urls")),
    path("events/", include("expense.events.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        *urls,
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns = urls
