from django import template
from customer.models import Notification

register = template.Library()

@register.simple_tag
def get_unread_notifications(user):
    if user.is_authenticated:
        return Notification.objects.filter(user=user, is_read=False)
    return []