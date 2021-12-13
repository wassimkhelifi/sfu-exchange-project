from django.shortcuts import render
from ..helpers import notification_helper


from ..models import Question

# Creating the questions view
def QuestionsView(request):
    questions_list = Question.objects.all()
    # TODO: can this be removed?
    notification_list = notification_helper.get_notifications(request.user)
    return render(request, 'exchange/questions.html', {
        'questions_list': questions_list,
        'notifications': notification_list,
    })