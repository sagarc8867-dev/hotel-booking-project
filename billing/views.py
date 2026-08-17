import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from reservations.models import Reservation
from .models import Payment
from .forms import PaymentForm
from urllib.parse import quote


def send_booking_confirmation_email(reservation, payment):
    subject = f"Booking Confirmed — Royal Stay (#{reservation.id})"
    html_content = render_to_string('emails/booking_confirmation.html', {
        'reservation': reservation,
        'payment': payment,
    })

    email = EmailMultiAlternatives(
        subject=subject,
        body=f"Your booking #{reservation.id} at Royal Stay is confirmed. Total paid: ₹{reservation.room_charges}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[reservation.guest.email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=True)


def payment_page(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment, _ = Payment.objects.get_or_create(
                reservation=reservation,
                defaults={'amount': reservation.room_charges},
            )
            payment.payment_method = form.cleaned_data['payment_method']

            if payment.payment_method == 'cash':
                payment.payment_status = 'pending'
                payment.transaction_id = ''
                reservation.status = 'pending'
            else:
                payment.payment_status = 'success'
                payment.transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
                payment.paid_at = timezone.now()
                reservation.status = 'confirmed'

            payment.save()
            reservation.save()

            send_booking_confirmation_email(reservation, payment)

            return redirect('confirmation', reservation_id=reservation.id)
    else:
        form = PaymentForm()

    upi_uri = (
        f"upi://pay?pa=royalstay@upi"
        f"&pn=Royal Stay Hotels"
        f"&am={reservation.room_charges}"
        f"&tn=Booking #{reservation.id} Room {reservation.room.room_number}"
        f"&cu=INR"
    )
    upi_qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=220x220&margin=0&data={quote(upi_uri, safe='')}"

    return render(request, 'user/payment.html', {
        'reservation': reservation,
        'form': form,
        'upi_qr_url': upi_qr_url,
    })