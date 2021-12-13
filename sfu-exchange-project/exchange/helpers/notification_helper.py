from django.db.models import Q
from ..models import Notification

def get_notifications(user):
    return Notification.objects.filter(
        Q(user_id=user.id) & Q(deleted=False)
    )

def create_notification(user, content):
    Notification.objects.create(
        notification_title=content['notification_title'], 
        notification_text=content['notification_text'],
        url = content['url'],
        user_id=user,
    )

def delete_notification(user, notification_id):
    Notification.objects.filter(
        Q(id=notification_id) & Q(user_id=user.id)
    ).update(deleted=True)
