from django.db.models import query
from django.shortcuts import render
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.paginator import Paginator

from ..models import Question, User
from ..helpers import notification_helper

# Creating the questions view
def SearchView(request):
    if request.method == 'GET':
        query_params = request.GET.get('q')

        if query_params:
            # Search these fields
            search_vector = SearchVector('title', 'question_text', 'tags__name')
            
            # Make the search inclusive OR for each term in the query
            search_query = SearchQuery("")
            for param in query_params.split():
                search_query = search_query | SearchQuery(param)

            # Perform the search
            questions = Question.objects.annotate(
                search=search_vector, 
                rank=SearchRank(search_vector, search_query)
            )
            
            questions = questions.filter(search=search_query).order_by("-rank", "-created_at")
        else:
            questions = Question.objects.order_by("-created_at")

        paginator = Paginator(questions, 10)
        page = request.GET.get("page")
        paginated_questions = paginator.get_page(page)

        notification_list = notification_helper.get_notifications(request.user)
        context = {
            'query': query_params if query_params != None else "",
            'questions_list': paginated_questions,
            'notifications': notification_list,
        }

        return render(request, 'exchange/questions.html', context)
