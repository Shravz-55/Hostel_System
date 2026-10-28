from django.contrib import admin
from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'floor', 'total_beds', 'available_beds', 'rent')
    list_filter = ('room_type', 'floor')
    search_fields = ('room_number',)
