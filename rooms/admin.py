
# Register your models here.
from django.contrib import admin
from .models import Room, RoomType


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'capacity')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'hotel', 'room_type', 'status')
    list_filter = ('status', 'hotel')