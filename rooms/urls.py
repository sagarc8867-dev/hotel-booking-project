from django.urls import path
from . import views


urlpatterns = [
    path("search/", views.search_rooms, name="search_rooms"),
    path("<int:pk>/", views.room_detail, name="room_detail"),
]
