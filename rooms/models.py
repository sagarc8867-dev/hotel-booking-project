from django.db import models
from hotels.models import Hotel
# Create your models here.

class RoomType(models.Model):
    name = models.CharField(max_length=100)  # Single, Double, Suite, Deluxe
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveSmallIntegerField(default=2)
    amenities = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Maintenance'),
        ('cleaning', 'Cleaning'),
    ]

    hotel = models.ForeignKey(Hotel, related_name='rooms', on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, related_name='rooms', on_delete=models.PROTECT)
    room_number = models.CharField(max_length=10)
    floor = models.PositiveSmallIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    price_override = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('hotel', 'room_number')
        ordering = ['hotel', 'floor', 'room_number']

    @property
    def price(self):
        return self.price_override or self.room_type.base_price

    def __str__(self):
        return f"{self.hotel.name} - Room {self.room_number}"