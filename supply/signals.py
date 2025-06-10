from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from supply.models import *
from customer.models import CustomerRequest

@receiver(post_save, sender=SupplyTransaction)
def update_stock_on_create(sender, instance, created, **kwargs):
    if created:
        item = instance.supply_item
        if instance.transaction_type == 'supply_in':
            item.quantity_in_stock += instance.quantity
        elif instance.transaction_type == 'supply_out':
            if item.quantity_in_stock < instance.quantity:
                raise ValueError("Not enough stock to complete this transaction.")
            item.quantity_in_stock -= instance.quantity
        elif instance.transaction_type == 'return':
            item.quantity_in_stock += instance.quantity
        elif instance.transaction_type == 'transfer':
            if item.quantity_in_stock < instance.quantity:
                raise ValueError("Not enough stock to complete this transfer.")
            item.quantity_in_stock -= instance.quantity
        item.save()

@receiver(post_delete, sender=SupplyTransaction)
def rollback_stock_on_delete(sender, instance, **kwargs):
    item = instance.supply_item
    if instance.transaction_type == 'supply_in':
        item.quantity_in_stock -= instance.quantity
    elif instance.transaction_type == 'supply_out':
        item.quantity_in_stock += instance.quantity
    elif instance.transaction_type == 'return':
        item.quantity_in_stock -= instance.quantity
    elif instance.transaction_type == 'transfer':
        item.quantity_in_stock += instance.quantity
    item.save()


@receiver(post_save, sender=CustomerRequest)
def notify_supply_managers_on_new_request(sender, instance, created, **kwargs):
    if created:
        # Notify supply managers of a new request
        supply_managers = User.objects.filter(groups__name='Supply Manager')
        for manager in supply_managers:
            NotificationFromCustomer.objects.create(
                user=manager,
                message=f"New request from {instance.customer.username} for {instance.supply_item.item_name}."
            )