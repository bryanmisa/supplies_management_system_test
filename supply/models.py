# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.conf import settings # Add this import

#region Managers (If you have custom managers for User types)
# Example:
class CustomerManager(UserManager): # Inherit from UserManager if needed
    def get_queryset(self):
        return super().get_queryset().filter(user_type='customer')

class SupplyManagerManager(UserManager): # Inherit from UserManager if needed
    def get_queryset(self):
        return super().get_queryset().filter(user_type='supply_manager')
#endregion Managers

# --- ADD THIS USER MODEL DEFINITION ---
class User(AbstractUser):
    # Add any custom fields you need here, for example:
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('supply_manager', 'Supply Manager'),
        ('admin', 'Administrator'), # Example
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # Use UserManager as the default manager
    objects = UserManager()
    # Add custom managers if you defined them above
    customers = CustomerManager()
    supply_managers = SupplyManagerManager()

    # You might want to remove the default email field if not needed or make it unique
    email = models.EmailField(unique=True) # Example: making email unique

    # Add any other methods or properties specific to your user

    def __str__(self):
        return self.username
# --- END OF USER MODEL DEFINITION ---

class Category(models.Model):   
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name

class SupplyItem(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('archived', 'Archived'),
    ]
    
    AVAILABILITY_CHOICES = [
        ('Available', 'Available'),
        ('Low Stock', 'Low in Supply'),
        ('Out of Stock', 'Out of Supply')
    ]

    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=200)
    item_code = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # Updated field
    description = models.TextField(blank=True)
    
    quantity_in_stock = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=0)
    unit_of_measure = models.CharField(max_length=50)
    
    # TODO: Change this to foreignkey
    location = models.CharField(max_length=100, blank=True)

    # TODO: Change this to foreignkey
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    # TODO: Change this to foreignkey
    currency = models.CharField(max_length=10, default='USD')

    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    last_purchase_date = models.DateField(null=True, blank=True)
    last_supplier_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    preferred_supplier = models.BooleanField(default=False)
    
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, # Use settings
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='added_supply_items' # Add related_name
    )
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    availability = models.CharField(choices=AVAILABILITY_CHOICES, default='Available')
    barcode = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='supply_images/', blank=True, null=True)
    expiration_date = models.DateField(null=True, blank=True)
    tags = models.CharField(max_length=200, blank=True)

    @property
    def total_value(self):
        return self.quantity_in_stock * self.unit_price
    
    def update_availability_status(self):
        """Updates the availability status based on quantity_in_stock and reorder_level."""
        if self.quantity_in_stock <= 0:
            self.availability = 'Out of Supply'
        elif self.quantity_in_stock <= self.reorder_level:
            self.availability = 'Low in Supply'
        else:
            self.availability = 'Available'
        self.save(update_fields=['availability'])
        
    def save(self, *args, **kwargs):
        if self.quantity_in_stock <= 0:
            self.availability = 'Out of Supply'
        elif self.quantity_in_stock <= self.reorder_level:
            self.availability = 'Low in Supply'
        else:
            self.availability = 'Available'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item_name} ({self.item_code})"
    
class SupplyTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('supply_in', 'Supply In'),
        ('supply_out', 'Supply Out'),
        ('return', 'Return (from other Location)'),
        ('transfer', 'Transfer (to other Location)'),
    ]

    supply_item = models.ForeignKey(SupplyItem, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    performed_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    remarks = models.TextField(blank=True)
    reference_number = models.CharField(max_length=100, blank=True)  # e.g., PO number or invoice
    source_location = models.CharField(max_length=100, blank=True)
    destination_location = models.CharField(max_length=100, blank=True)
    
    def clean(self):
        super().clean() # Call parent clean method
        # Validate stock quantity for supply_out and transfer
        # if self.transaction_type in ['supply_out', 'transfer']:
        #     if self.supply_item.quantity_in_stock < self.quantity:
        #         raise ValidationError(f"Not enough supplies available for '{self.supply_item.item_name}")
        pass # No specific logic here, but you can add any custom validation if needed

    def save(self, *args, **kwargs):
        # Call clean to ensure validation is applied before saving
        self.clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.transaction_type} - {self.supply_item.item_name} ({self.quantity}) on {self.date.strftime('%Y-%m-%d')}"
    
