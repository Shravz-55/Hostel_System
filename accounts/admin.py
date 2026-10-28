from django.contrib import admin
from .models import Warden


@admin.register(Warden)
class WardenAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'username', 'created_at']
    search_fields = ['name', 'email', 'username']
