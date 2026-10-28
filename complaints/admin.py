from django.contrib import admin
from .models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['title', 'student', 'status', 'date']
    list_filter = ['status']
    search_fields = ['title', 'student__name']
