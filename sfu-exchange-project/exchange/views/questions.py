from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import F

from ..models import Question

# Creating the questions view
def QuestionsView(request):
    questions_list = Question.objects.all()
    return render(request, 'exchange/questions.html', {
        'questions_list': questions_list,
    })
