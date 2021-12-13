import django
from django.core import paginator
from django.db.models import fields, query
from django.db.models.aggregates import Count, Sum
from django.db.models.query_utils import Q
from django.shortcuts import render
from django.core.paginator import Paginator
from ..models import Question
from django.views.generic.list import ListView


# Creating the questions view
def QuestionsView(request):
    f = request.GET.get('filter','').strip("'")

    # Hella jank but it was the fastest way of doing this 
    if f == 'popular':
        questions_list = Question.objects.order_by('-votes')
    elif f =='unanswered':
        questions_list = Question.objects.annotate(count = Count('answer')).filter(
            Q(count=0)
        )
    else:
        questions_list = Question.objects.order_by('-created_at')

    print(questions_list[0])

    paginator = Paginator(questions_list, 10)
    page = request.GET.get("page")
    print(page)
    paginated_questions = paginator.get_page(page)

    return render(request, 'exchange/questions.html', {
        'questions_list': paginated_questions,
    })