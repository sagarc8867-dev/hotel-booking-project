from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from guests.forms import GuestForm
from guests.models import Guest
from rooms.models import Room
from .models import Reservation

@login_required
def booking_form(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    check_in = request.GET.get('check_in') or request.POST.get('check_in')
    check_out = request.GET.get('check_out') or request.POST.get('check_out')
    guests = request.GET.get('guests') or request.POST.get('guests') or 1

    initial = {}
    if request.user.is_authenticated:
        existing_guest = Guest.objects.filter(user=request.user).first()
        if existing_guest:
            initial = {
                'first_name': existing_guest.first_name,
                'last_name': existing_guest.last_name,
                'email': existing_guest.email,
                'phone': existing_guest.phone,
                'id_proof_type': existing_guest.id_proof_type,
                'id_proof_number': existing_guest.id_proof_number,
                'address': existing_guest.address,
            }
        else:
            initial = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }

    if request.method == 'POST':
        form = GuestForm(request.POST)
        post_check_in = request.POST.get('check_in')
        post_check_out = request.POST.get('check_out')

        if not post_check_in or not post_check_out or post_check_in == 'None' or post_check_out == 'None':
            form.add_error(None, 'Please select valid check-in and check-out dates.')
        elif form.is_valid():
            guest = form.save(commit=False)

            if request.user.is_authenticated:
                existing_guest = Guest.objects.filter(user=request.user).first()
                if existing_guest:
                    guest.pk = existing_guest.pk
                    guest.created_at = existing_guest.created_at
                guest.user = request.user

            guest.save()

            reservation = Reservation.objects.create(
                guest=guest,
                room=room,
                check_in_date=post_check_in,
                check_out_date=post_check_out,
                num_guests=guests,
                special_requests=request.POST.get('special_requests', ''),
                status='pending',
            )
            return redirect('payment_page', reservation_id=reservation.id)
    else:
        form = GuestForm(initial=initial)

    context = {
        'room': room,
        'check_in': check_in,
        'check_out': check_out,
        'guests': guests,
        'form': form,
    }
    return render(request, 'user/booking.html', context)


def confirmation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    messages.success(
        request,
        f"🎉 Booking confirmed! Enjoy your stay at {reservation.room.hotel.name}, "
        f"{reservation.guest.first_name}."
    )
    return render(request, 'user/confirmation.html', {'reservation': reservation})


@login_required
def my_bookings(request):
    reservations = Reservation.objects.select_related(
        'room', 'room__hotel'
    ).filter(
        guest__user=request.user
    ).order_by('-booking_date')

    return render(request, 'user/my_bookings.html', {'reservations': reservations})