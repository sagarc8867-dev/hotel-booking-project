from django.contrib import messages
from django.db.models import Q, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from hotels.models import Hotel
from hotels.forms import HotelForm
from rooms.models import Room
from rooms.forms import RoomForm
from guests.models import Guest
from guests.forms import GuestForm
from reservations.models import Reservation
from billing.models import Payment
from housekeeping.models import Housekeeping
from housekeeping.forms import HousekeepingForm

from .decorators import staff_required


# ===========================
# DASHBOARD
# ===========================

@staff_required
def dashboard(request):
    context = {
        "hotel_count": Hotel.objects.count(),
        "room_count": Room.objects.count(),
        "available_room_count": Room.objects.filter(status="available").count(),
        "guest_count": Guest.objects.count(),
        "reservation_count": Reservation.objects.count(),
        "pending_count": Reservation.objects.filter(status="pending").count(),
        "checked_in_count": Reservation.objects.filter(status="checked_in").count(),
        "housekeeping_pending_count": Housekeeping.objects.filter(status="pending").count(),
        "total_revenue": Payment.objects.filter(payment_status="success").aggregate(total=Sum("amount"))["total"] or 0,
        "recent_reservations": Reservation.objects.select_related("guest", "room", "room__hotel").order_by("-booking_date")[:8],
        "active": "dashboard",
    }
    return render(request, "admin/dashboard.html", context)


# ===========================
# HOTELS
# ===========================

@staff_required
def hotel_list(request):
    search = request.GET.get("search", "")
    hotels = Hotel.objects.all()

    if search:
        hotels = hotels.filter(
            Q(name__icontains=search) |
            Q(city__icontains=search) |
            Q(state__icontains=search) |
            Q(country__icontains=search)
        )

    return render(request, "admin/hotels.html", {"hotels": hotels, "search": search, "active": "hotels"})


@staff_required
def hotel_add(request):
    if request.method == "POST":
        form = HotelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Hotel added successfully.")
            return redirect("admin_hotel_list")
    else:
        form = HotelForm()

    return render(request, "forms.html", {
        "form": form,
        "title": "Add Hotel",
        "subtitle": "Enter hotel details.",
        "cancel_url": reverse("admin_hotel_list"),
    })


@staff_required
def hotel_edit(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)

    if request.method == "POST":
        form = HotelForm(request.POST, instance=hotel)
        if form.is_valid():
            form.save()
            messages.success(request, "Hotel updated successfully.")
            return redirect("admin_hotel_list")
    else:
        form = HotelForm(instance=hotel)

    return render(request, "forms.html", {
        "form": form,
        "title": "Edit Hotel",
        "subtitle": "Update hotel details.",
        "cancel_url": reverse("admin_hotel_list"),
    })


@staff_required
def hotel_delete(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)

    if request.method == "POST":
        hotel.delete()
        messages.success(request, "Hotel deleted successfully.")
        return redirect("admin_hotel_list")

    return render(request, "confirm_delete.html", {
        "title": "Delete Hotel",
        "subtitle": "Are you sure you want to delete this hotel? This cannot be undone.",
        "object_display": [("Name", hotel.name), ("City", hotel.city)],
        "cancel_url": reverse("admin_hotel_list"),
    })


# ===========================
# ROOMS
# ===========================

@staff_required
def room_list(request):
    search = request.GET.get("search", "")
    rooms = Room.objects.select_related("hotel", "room_type")

    if search:
        rooms = rooms.filter(
            Q(room_number__icontains=search) |
            Q(hotel__name__icontains=search) |
            Q(hotel__city__icontains=search) |
            Q(room_type__name__icontains=search)
        )

    return render(request, "admin/rooms.html", {"rooms": rooms, "search": search, "active": "rooms"})


@staff_required
def room_add(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Room added successfully.")
            return redirect("admin_room_list")
    else:
        form = RoomForm()

    return render(request, "forms.html", {
        "form": form,
        "title": "Add Room",
        "subtitle": "Create a new room.",
        "cancel_url": reverse("admin_room_list"),
    })


@staff_required
def room_edit(request, pk):
    room = get_object_or_404(Room, pk=pk)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, "Room updated successfully.")
            return redirect("admin_room_list")
    else:
        form = RoomForm(instance=room)

    return render(request, "forms.html", {
        "form": form,
        "title": "Edit Room",
        "subtitle": "Update room details.",
        "cancel_url": reverse("admin_room_list"),
    })


@staff_required
def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)

    if request.method == "POST":
        room.delete()
        messages.success(request, "Room deleted successfully.")
        return redirect("admin_room_list")

    return render(request, "confirm_delete.html", {
        "title": "Delete Room",
        "subtitle": "Are you sure you want to delete this room?",
        "object_display": [
            ("Hotel", room.hotel.name),
            ("Room", room.room_number),
            ("Type", room.room_type.name),
        ],
        "cancel_url": reverse("admin_room_list"),
    })


# ===========================
# GUESTS
# ===========================

@staff_required
def guest_list(request):
    search = request.GET.get("search", "")
    guests = Guest.objects.all()

    if search:
        guests = guests.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )

    return render(request, "admin/guests.html", {"guests": guests, "search": search, "active": "guests"})


@staff_required
def guest_add(request):
    if request.method == "POST":
        form = GuestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Guest added successfully.")
            return redirect("admin_guest_list")
    else:
        form = GuestForm()

    return render(request, "forms.html", {
        "form": form,
        "title": "Add Guest",
        "subtitle": "Create a new guest profile.",
        "cancel_url": reverse("admin_guest_list"),
    })


@staff_required
def guest_edit(request, pk):
    guest = get_object_or_404(Guest, pk=pk)

    if request.method == "POST":
        form = GuestForm(request.POST, instance=guest)
        if form.is_valid():
            form.save()
            messages.success(request, "Guest updated successfully.")
            return redirect("admin_guest_list")
    else:
        form = GuestForm(instance=guest)

    return render(request, "forms.html", {
        "form": form,
        "title": "Edit Guest",
        "subtitle": "Update guest details.",
        "cancel_url": reverse("admin_guest_list"),
    })


@staff_required
def guest_delete(request, pk):
    guest = get_object_or_404(Guest, pk=pk)

    if request.method == "POST":
        guest.delete()
        messages.success(request, "Guest deleted successfully.")
        return redirect("admin_guest_list")

    return render(request, "confirm_delete.html", {
        "title": "Delete Guest",
        "subtitle": "Are you sure you want to delete this guest profile?",
        "object_display": [
            ("Name", f"{guest.first_name} {guest.last_name}"),
            ("Email", guest.email),
        ],
        "cancel_url": reverse("admin_guest_list"),
    })


# ===========================
# RESERVATIONS
# ===========================

ALLOWED_TRANSITIONS = {
    "pending": ["confirmed", "cancelled"],
    "confirmed": ["checked_in", "cancelled"],
    "checked_in": ["checked_out"],
}


@staff_required
def reservation_list(request):
    search = request.GET.get("search", "")
    reservations = Reservation.objects.select_related("guest", "room", "room__hotel")

    if search:
        reservations = reservations.filter(
            Q(guest__first_name__icontains=search) |
            Q(guest__last_name__icontains=search) |
            Q(room__room_number__icontains=search) |
            Q(room__hotel__name__icontains=search)
        )

    return render(request, "admin/reservations.html", {
        "reservations": reservations,
        "search": search,
        "active": "reservations",
    })


@staff_required
def reservation_update_status(request, pk, status):
    reservation = get_object_or_404(Reservation, pk=pk)
    valid_statuses = dict(Reservation.STATUS_CHOICES)

    if request.method == "POST" and status in valid_statuses:
        allowed_next = ALLOWED_TRANSITIONS.get(reservation.status, [])

        if status in allowed_next:
            reservation.status = status

            if status == "checked_in":
                reservation.actual_check_in_time = timezone.now()
                reservation.room.status = "occupied"
                reservation.room.save()

            elif status == "checked_out":
                reservation.actual_check_out_time = timezone.now()
                reservation.room.status = "cleaning"
                reservation.room.save()
                Housekeeping.objects.create(
                    room=reservation.room,
                    status="pending",
                    remarks=f"Auto-created after checkout of reservation #{reservation.id}",
                )

            elif status == "cancelled" and reservation.room.status == "occupied":
                reservation.room.status = "available"
                reservation.room.save()

            reservation.save()
            messages.success(request, f"Reservation #{reservation.id} marked as {valid_statuses[status]}.")
        else:
            messages.error(request, "That status change isn't allowed from the current status.")

    return redirect("admin_reservation_list")


@staff_required
def reservation_delete(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)

    if request.method == "POST":
        reservation.delete()
        messages.success(request, "Reservation deleted successfully.")
        return redirect("admin_reservation_list")

    return render(request, "confirm_delete.html", {
        "title": "Delete Reservation",
        "subtitle": "Are you sure you want to delete this reservation?",
        "object_display": [
            ("Guest", str(reservation.guest)),
            ("Room", str(reservation.room)),
            ("Stay", f"{reservation.check_in_date} → {reservation.check_out_date}"),
        ],
        "cancel_url": reverse("admin_reservation_list"),
    })


# ===========================
# BILLING
# ===========================

@staff_required
def billing_list(request):
    search = request.GET.get("search", "")
    payments = Payment.objects.select_related("reservation", "reservation__guest").order_by("-paid_at")

    if search:
        payments = payments.filter(
            Q(transaction_id__icontains=search) |
            Q(reservation__guest__first_name__icontains=search) |
            Q(reservation__guest__last_name__icontains=search)
        )

    total_collected = payments.filter(payment_status="success").aggregate(total=Sum("amount"))["total"] or 0

    return render(request, "admin/billing.html", {
        "payments": payments,
        "search": search,
        "total_collected": total_collected,
        "success_count": payments.filter(payment_status="success").count(),
        "pending_count": payments.filter(payment_status="pending").count(),
        "active": "billing",
    })


# ===========================
# HOUSEKEEPING
# ===========================

@staff_required
def housekeeping_list(request):
    search = request.GET.get("search", "")
    tasks = Housekeeping.objects.select_related("room", "room__hotel")

    if search:
        tasks = tasks.filter(
            Q(room__room_number__icontains=search) |
            Q(staff_name__icontains=search) |
            Q(room__hotel__name__icontains=search)
        )

    return render(request, "admin/housekeeping.html", {"tasks": tasks, "search": search, "active": "housekeeping"})


@staff_required
def housekeeping_add(request):
    if request.method == "POST":
        form = HousekeepingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Housekeeping task added successfully.")
            return redirect("admin_housekeeping_list")
    else:
        form = HousekeepingForm()

    return render(request, "forms.html", {
        "form": form,
        "title": "Add Housekeeping Task",
        "subtitle": "Assign a cleaning or maintenance task.",
        "cancel_url": reverse("admin_housekeeping_list"),
    })


@staff_required
def housekeeping_edit(request, pk):
    task = get_object_or_404(Housekeeping, pk=pk)

    if request.method == "POST":
        form = HousekeepingForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Housekeeping task updated successfully.")
            return redirect("admin_housekeeping_list")
    else:
        form = HousekeepingForm(instance=task)

    return render(request, "forms.html", {
        "form": form,
        "title": "Edit Housekeeping Task",
        "subtitle": "Update task status and remarks.",
        "cancel_url": reverse("admin_housekeeping_list"),
    })


@staff_required
def housekeeping_delete(request, pk):
    task = get_object_or_404(Housekeeping, pk=pk)

    if request.method == "POST":
        task.delete()
        messages.success(request, "Housekeeping task deleted successfully.")
        return redirect("admin_housekeeping_list")

    return render(request, "confirm_delete.html", {
        "title": "Delete Housekeeping Task",
        "subtitle": "Are you sure you want to delete this task?",
        "object_display": [
            ("Room", str(task.room)),
            ("Status", task.get_status_display()),
        ],
        "cancel_url": reverse("admin_housekeeping_list"),
    })
