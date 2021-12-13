from django.core import paginator
from django.db.models import query
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from ..models import Question

# Creating the questions view
def QuestionsView(request):
    questions_list = Question.objects.all()

    paginator = Paginator(questions_list, 10)
    page = request.GET.get("page")
    paginated_questions = paginator.get_page(page)

    return render(request, 'exchange/questions.html', {
        'questions_list': paginated_questions,
    })