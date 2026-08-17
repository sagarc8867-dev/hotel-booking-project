
# Create your models here.
from django.db import models
from guests.models import Guest
from rooms.models import Room


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ]

    guest = models.ForeignKey(Guest, related_name='reservations', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='reservations', on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    num_guests = models.PositiveSmallIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booking_date = models.DateTimeField(auto_now_add=True)
    special_requests = models.TextField(blank=True)
    actual_check_in_time = models.DateTimeField(null=True, blank=True)
    actual_check_out_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-booking_date']

    @property
    def nights(self):
        return max((self.check_out_date - self.check_in_date).days, 1)

    @property
    def room_charges(self):
        return self.room.price * self.nights

    def __str__(self):
        return f"Reservation #{self.id} - {self.guest} - {self.room}"