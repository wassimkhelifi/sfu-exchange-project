from django.shortcuts import render
from ..helpers import notification_helper


from ..models import Question

# Creating the notifications view
def NotificationsView(request):
    questions_list = Question.objects.all()
    # TODO: can this be removed?
    notification_list = notification_helper.get_notifications(request.user)
    return render(request, 'exchange/notifications.html', {
        'questions_list': questions_list,
        'notifications': notification_list,
    })