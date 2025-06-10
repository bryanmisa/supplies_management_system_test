# customer/admin.py
from django.contrib import admin
from .models import * # Import from local models

@admin.register(CustomerRequest)
class CustomerRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'supply_item', 'customer', 'requested_quantity', 'request_date', 'status', 'performed_by')
    search_fields = ('supply_item__item_name', 'customer__username', 'status', 'id') # Search by item name, customer username, status, or ID
    list_filter = ('status', 'request_date', 'customer') # Filter by status, date, or customer
    # Use __ notation for foreign keys in autocomplete_fields
    autocomplete_fields = ['supply_item', 'customer', 'performed_by']
    list_per_page = 25 # Optional: items per page

    # Make fields read-only in admin after creation if needed
    # readonly_fields = ('request_date', 'customer', 'supply_item', 'requested_quantity')

    fieldsets = (
        (None, {
            'fields': ('supply_item', 'customer', 'requested_quantity')
        }),
        ('Status & Processing', {
            'fields': ('status', 'rejection_reason', 'performed_by', 'request_date')
        }),
    )
    # Make request_date read-only on the edit page
    readonly_fields = ('request_date',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    search_fields = ('user__username', 'message')   # Search by user username or message content
