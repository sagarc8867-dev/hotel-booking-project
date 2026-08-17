from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


def staff_required(view_func):
    """Only allow authenticated staff (is_staff=True) users through.
    Anyone else is redirected to the staff login page (or home, with a
    message, if they are logged in as a regular guest)."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{reverse('admin_login')}?next={request.path}")
        if not request.user.is_staff:
            messages.error(request, "You don't have permission to access the staff dashboard.")
            return redirect('home')
        return view_func(request, *args, **kwargs)

    return wrapper
