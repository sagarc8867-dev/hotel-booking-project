from django.contrib import admin
from .models import Housekeeping


@admin.register(Housekeeping)
class HousekeepingAdmin(admin.ModelAdmin):
    list_display = ('room', 'staff_name', 'status', 'updated_at')
    list_filter = ('status',)
