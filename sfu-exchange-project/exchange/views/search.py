from django.db.models import query
from django.shortcuts import render
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from ..models import Question, User



# Creating the questions view
def SearchView(request):
    if request.method == 'GET':
        query_params = request.GET.get('q')

        if query_params:
            # Search these fields
            search_vector = SearchVector('title', 'question_text', 'tags__name')
            
            # Make the search inclusive OR for each term in the query
            or_query_params = ' | '.join(query_params.split())
            search_query = SearchQuery(or_query_params, search_type='raw')

            # Perform the search
            questions = Question.objects.annotate(
                search=search_vector, 
                rank=SearchRank(search_vector, search_query)
            )
            
            questions = questions.filter(search=search_query).order_by("-rank", "-created_at")
        else:
            questions = Question.objects.order_by("-created_at")

        return render(request, 'exchange/search.html', {
            'query': query_params if query_params != None else "",
            'search_results': questions,
        })
