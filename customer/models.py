# customer/models.py
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings # Import settings
from supply.models import SupplyItem # Import SupplyItem from supply app


class CustomerRequest(models.Model):
    supply_item = models.ForeignKey(
        SupplyItem,
        on_delete=models.CASCADE,
        related_name='customer_requests'
    )
    # Use settings.AUTH_USER_MODEL for ForeignKey to User
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='requests'
    )
    requested_quantity = models.IntegerField()
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('delivered', 'Delivered'),
        ],
        default='pending'
    )
    rejection_reason = models.TextField(blank=True, null=True)
    # Use settings.AUTH_USER_MODEL for ForeignKey to User
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='performed_customer_requests' # Add related_name to avoid clash
    )

    def __str__(self):
        # Ensure customer attribute exists before accessing username
        customer_name = self.customer.username if self.customer else "Unknown Customer"
        item_name = self.supply_item.item_name if self.supply_item else "Unknown Item"
        return f"Request for {item_name} by {customer_name}"


