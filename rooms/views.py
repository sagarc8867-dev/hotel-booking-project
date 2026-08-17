from django.shortcuts import render, get_object_or_404

from .models import Room
from .forms import RoomSearchForm
from reservations.models import Reservation


# ===========================
# ROOM DETAILS (public)
# ===========================

def room_detail(request, pk):

    room = get_object_or_404(
        Room.objects.select_related("hotel", "room_type"),
        pk=pk
    )

    return render(
        request,
        "user/room_detail.html",
        {
            "room": room
        }
    )


# ===========================
# SEARCH ROOMS (public)
# ===========================

def search_rooms(request):

    form = RoomSearchForm(request.GET or None)

    rooms = Room.objects.none()

    searched = False

    if form.is_valid():

        searched = True

        city = form.cleaned_data.get("city")
        check_in = form.cleaned_data.get("check_in")
        check_out = form.cleaned_data.get("check_out")
        guests = form.cleaned_data.get("guests")

        rooms = Room.objects.select_related(
            "hotel",
            "room_type"
        ).exclude(
            status="maintenance"
        )

        if city:
            rooms = rooms.filter(
                hotel__city__icontains=city
            )

        if guests:
            rooms = rooms.filter(
                room_type__capacity__gte=guests
            )

        if check_in and check_out:

            booked_rooms = Reservation.objects.filter(
                status__in=[
                    "pending",
                    "confirmed",
                    "checked_in",
                ],
                check_in_date__lt=check_out,
                check_out_date__gt=check_in,
            ).values_list(
                "room_id",
                flat=True
            )

            rooms = rooms.exclude(
                id__in=booked_rooms
            )

    return render(
        request,
        "user/search.html",
        {
            "form": form,
            "rooms": rooms,
            "searched": searched,
        }
    )
