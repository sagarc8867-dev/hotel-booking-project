from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Hotel


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'star_rating', 'contact_email')
    search_fields = ('name', 'city')