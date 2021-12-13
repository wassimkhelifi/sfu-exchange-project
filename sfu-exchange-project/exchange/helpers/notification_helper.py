from ..models import Notification

def get_notifications(user):
    return Notification.objects.filter(user_id=user.id).order_by("-created_at")

def create_notification(user, content):
    Notification.objects.create(
        notification_title=content['notification_title'], 
        notification_text=content['notification_text'],
        notification_type=content['notification_type'],
        url = content['url'],
        user_id=user,
    )
