from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:room_id>/', views.booking_form, name='booking_form'),
    path('confirmation/<int:reservation_id>/', views.confirmation, name='confirmation'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]
