from django.shortcuts import render, get_object_or_404

from .models import Hotel
from rooms.models import Room


# ===========================
# HOME PAGE
# ===========================

def home(request):
    hotels = Hotel.objects.all()[:6]

    featured_rooms = Room.objects.select_related(
        "hotel", "room_type"
    ).filter(
        status="available"
    ).order_by("-id")[:4]

    context = {
        "hotels": hotels,
        "featured_rooms": featured_rooms,
    }

    return render(request, "user/home.html", context)


# ===========================
# HOTEL DETAILS (public)
# ===========================

def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)

    return render(
        request,
        "user/hotel_detail.html",
        {
            "hotel": hotel
        }
    )
