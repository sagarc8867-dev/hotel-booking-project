from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'guest', 'room', 'check_in_date', 'check_out_date', 'status')
    list_filter = ('status',)