from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from tasks.views import logout_view  # GET-friendly logout

urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("accounts/logout/", logout_view, name="logout"),

    # App (NOTE: include ONLY the tasks app here; nothing else!)
    path("", include(("tasks.urls", "tasks"), namespace="tasks")),
]
