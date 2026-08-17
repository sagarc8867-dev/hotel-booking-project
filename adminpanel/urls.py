from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="admin_dashboard"),

    path("hotels/", views.hotel_list, name="admin_hotel_list"),
    path("hotels/add/", views.hotel_add, name="admin_hotel_add"),
    path("hotels/<int:pk>/edit/", views.hotel_edit, name="admin_hotel_edit"),
    path("hotels/<int:pk>/delete/", views.hotel_delete, name="admin_hotel_delete"),

    path("rooms/", views.room_list, name="admin_room_list"),
    path("rooms/add/", views.room_add, name="admin_room_add"),
    path("rooms/<int:pk>/edit/", views.room_edit, name="admin_room_edit"),
    path("rooms/<int:pk>/delete/", views.room_delete, name="admin_room_delete"),

    path("guests/", views.guest_list, name="admin_guest_list"),
    path("guests/add/", views.guest_add, name="admin_guest_add"),
    path("guests/<int:pk>/edit/", views.guest_edit, name="admin_guest_edit"),
    path("guests/<int:pk>/delete/", views.guest_delete, name="admin_guest_delete"),

    path("reservations/", views.reservation_list, name="admin_reservation_list"),
    path("reservations/<int:pk>/status/<str:status>/", views.reservation_update_status, name="admin_reservation_status"),
    path("reservations/<int:pk>/delete/", views.reservation_delete, name="admin_reservation_delete"),

    path("billing/", views.billing_list, name="admin_billing_list"),

    path("housekeeping/", views.housekeeping_list, name="admin_housekeeping_list"),
    path("housekeeping/add/", views.housekeeping_add, name="admin_housekeeping_add"),
    path("housekeeping/<int:pk>/edit/", views.housekeeping_edit, name="admin_housekeeping_edit"),
    path("housekeeping/<int:pk>/delete/", views.housekeeping_delete, name="admin_housekeeping_delete"),
]
