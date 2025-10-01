# todoproject/views.py
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required

@require_GET
@login_required
def logout_get(request):
    """
    Log out on GET, then redirect to the login page.
    NOTE: This trades a bit of security for convenience.
    """
    logout(request)
    return redirect("login")
