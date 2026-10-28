from django.contrib import admin
from .models import Fee


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ['student', 'month', 'amount', 'status', 'payment_date']
    list_filter = ['status', 'month']
    search_fields = ['student__name']
