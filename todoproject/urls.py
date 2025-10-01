# todoproject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from .views import logout_get  # <-- our GET-based logout

urlpatterns = [
    path("admin/", admin.site.urls),

    # Our GET logout must come BEFORE the auth include so it wins the match
    path("accounts/logout/", logout_get, name="logout"),

    # Built-in auth routes: /accounts/login/, password reset, etc.
    path(
        "accounts/signup/",
        CreateView.as_view(
            template_name="registration/signup.html",
            form_class=UserCreationForm,
            success_url=reverse_lazy("login"),
        ),
        name="signup",
    ),
    path("accounts/", include("django.contrib.auth.urls")),

    # Your app
    path("", include(("tasks.urls", "tasks"), namespace="tasks")),
]
