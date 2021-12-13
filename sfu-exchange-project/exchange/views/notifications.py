from django.shortcuts import render
from ..helpers import notification_helper


from ..models import Notification

# Creating the notifications view
def NotificationsView(request):
    notification_list = notification_helper.get_notifications(request.user)
    return render(request, 'exchange/notifications.html', {
        "notifications": notification_list,
    })