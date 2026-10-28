from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'college', 'room', 'joining_date']
    list_filter = ['college', 'course', 'room']
    search_fields = ['name', 'email', 'username']
