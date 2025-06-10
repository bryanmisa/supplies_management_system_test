from django import template
from supply.models import NotificationFromCustomer

register = template.Library()

@register.simple_tag
def get_unread_notifications(user):
    if user.is_authenticated:
        return NotificationFromCustomer.objects.filter(user=user, is_read=False).order_by('-created_at')
    return []