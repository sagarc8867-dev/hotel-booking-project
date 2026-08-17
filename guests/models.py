from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here."
from django.conf import settings
from django.db import models


class Guest(models.Model):

    ID_PROOF_CHOICES = [
        ('aadhar', 'Aadhar Card'),
        ('pan', 'PAN Card'),
        ('passport', 'Passport'),
        ('driving_license', 'Driving License'),
        ('voter_id', 'Voter ID'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='guest_profile',
    )
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=15)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(120)]
    )
    id_proof_type = models.CharField(max_length=50, choices=ID_PROOF_CHOICES)
    id_proof_number = models.CharField(max_length=16)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"