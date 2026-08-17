from django.urls import path
from . import views

urlpatterns = [
    path('pay/<int:reservation_id>/', views.payment_page, name='payment_page'),
]