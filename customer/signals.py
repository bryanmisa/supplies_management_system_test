from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from django.contrib.auth import get_user_model  # Use get_user_model to reference the custom user model
import logging

from customer.models import CustomerRequest, Notification
from supply.models import SupplyTransaction

logger = logging.getLogger(__name__)

User = get_user_model()  # Get the custom user model dynamically

@receiver(post_save, sender=CustomerRequest)
def create_supply_out_transaction_on_delivery(sender, instance, created, **kwargs):
    """
    Creates a 'supply_out' transaction when a CustomerRequest status
    is changed to 'delivered' and updates the quantity of the supply item.
    """
    if not created and instance.status == 'delivered':
        # Use transaction.atomic to ensure both operations succeed or fail together
        with transaction.atomic():
            # Check if a transaction for this delivery already exists to prevent duplicates
            if not SupplyTransaction.objects.filter(remarks__icontains=f"Request ID: {instance.pk}", transaction_type='supply_out').exists():
                logger.info(f"Request {instance.pk} marked delivered. Creating supply_out transaction.")
                
                # Create the supply_out transaction
                SupplyTransaction.objects.create(
                    supply_item=instance.supply_item,
                    transaction_type='supply_out',
                    quantity=instance.requested_quantity,
                    performed_by=instance.performed_by,  # User who marked as delivered
                    remarks=f"Delivered to customer: {instance.customer.username} (Request ID: {instance.pk})"
                )
                
                # Deduct the quantity from the supply item
                instance.supply_item.quantity_in_stock -= instance.requested_quantity
                instance.supply_item.save()
                logger.info(f"Updated quantity_in_stock for {instance.supply_item.item_name}. New stock: {instance.supply_item.quantity_in_stock}")
            else:
                logger.warning(f"Supply_out transaction for Request ID {instance.pk} already exists. Skipping creation.")
                
@receiver(post_save, sender=CustomerRequest)
def create_notifications(sender, instance, created, **kwargs):
    if created:
        # Notify supply managers of a new request
        supply_managers = User.objects.filter(groups__name='Supply Manager')  # Use the custom user model
        for manager in supply_managers:
            Notification.objects.create(
                user=manager,
                message=f"New request from {instance.customer.username} for {instance.supply_item.item_name}."
            )   
    else:
        # Notify the customer of status changes
        if instance.status == 'approved':
            Notification.objects.create(
                user=instance.customer,
                message=f"Your request for {instance.supply_item.item_name} has been approved."
            )
        elif instance.status == 'delivered':
            Notification.objects.create(
                user=instance.customer,
                message=f"Your request for {instance.supply_item.item_name} has been delivered."
            )
        elif instance.status == 'rejected':
            Notification.objects.create(
                user=instance.customer,
                message=f"Your request for {instance.supply_item.item_name} has been rejected."
            )
            
