from django.db.models import query
from django.shortcuts import render
from django.db.models import Q
from ..models import Question, User



# Creating the questions view
def SearchView(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        user_ids = User.objects.filter(
            Q(username__icontains=query)   | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        )
        search_results = Question.objects.filter(
            Q(title__icontains=query) | Q(user_id__in=user_ids)
        )
        return render(request, 'exchange/search.html', {
            'query': query,
            'search_results': search_results,
        })
