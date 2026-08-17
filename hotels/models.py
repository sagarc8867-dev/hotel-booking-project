from django.db import models

# Create your models here.
class Hotel(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='India')
    star_rating = models.PositiveSmallIntegerField(default=3)
    description = models.TextField(blank=True)
    amenities = models.JSONField(default=list, blank=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.city})"