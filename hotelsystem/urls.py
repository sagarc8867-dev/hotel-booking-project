"""
URL configuration for hotelsystem project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    # Django's built-in admin (superuser database access)
    path("django-admin/", admin.site.urls),

    # Guest / staff authentication
    path("accounts/", include("accounts.urls")),

    # Custom staff dashboard (hotels, rooms, guests, reservations, billing, housekeeping)
    path("manage/", include("adminpanel.urls")),

    # Public, guest-facing site
    path("", include("hotels.urls")),
    path("rooms/", include("rooms.urls")),
    path("reservations/", include("reservations.urls")),
    path("billing/", include("billing.urls")),

]
