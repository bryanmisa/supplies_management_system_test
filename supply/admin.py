# Register your models here.
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from supply.models import *


from django.contrib import admin
# Import UserAdmin
from django.contrib.auth.admin import UserAdmin
# Import your custom User model and other models
from .models import User, SupplyItem, Supplier, SupplyTransaction, Category
# Import Group and Permission if you need them later (already present)
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# --- Add this section for User Admin ---
class CustomUserAdmin(UserAdmin):
    # Add your custom fields to the list display, fieldsets, etc.
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'user_type') # Added user_type
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_type') # Added user_type
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Info', {'fields': ('user_type', 'contact_number', 'address')}), # Add a new section for custom fields
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Info', {'fields': ('user_type', 'contact_number', 'address')}), # Add custom fields to the 'add user' form
    )

# Register your custom User model with the custom admin class
admin.site.register(User, CustomUserAdmin)
# --- End User Admin section ---

@admin.register(SupplyItem)
class SupplyItemAdmin(admin.ModelAdmin):
    list_display = ('item_id','item_name', 'item_code', 'quantity_in_stock', 'unit_price', 'status')
    search_fields = ('item_name', 'item_code', 'category')
    list_filter = ('status', 'category', 'supplier')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_email', 'phone')
    search_fields = ('name',)


@admin.register(SupplyTransaction)
class SupplyTransactionAdmin(admin.ModelAdmin):
    list_display = ('supply_item', 'transaction_type', 'quantity', 'date', 'performed_by')
    search_fields = ('supply_item__item_name', 'transaction_type', 'reference_number')
    list_filter = ('transaction_type', 'date')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)


# @admin.register(Notification)
# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ('user', 'message', 'is_read', 'created_at')
#     search_fields = ('user__username', 'message')
#     list_filter = ('is_read', 'created_at')

