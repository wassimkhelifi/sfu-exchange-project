from django.core import paginator
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Count, Sum, query
from django.db.models.functions import Coalesce
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from ..models import User
from ..helpers import notification_helper


def UsersView(request, page=""):
    if request.method == "GET":
        query_params = request.GET.get("q")
        query_params = "" if not query_params else query_params

        # Search these fields
        search_vector = SearchVector('username', 'email', 'first_name', 'last_name', 'bio', 'roles__name', 'faculty_id__name')
        
        # Make the search inclusive OR for each term in the query
        or_query_params = []
        or_query_params = '* | '.join(query_params.split() if query_params != None else "")

        search_query = SearchQuery("")
        for param in query_params.split():
            search_query = search_query | SearchQuery(param)

        print("@@SEARCH: search_query:", search_query)
        # Perform the search
        users = User.objects.annotate(
            search=search_vector, 
            rank=SearchRank(search_vector, search_query),
            num_posts=Count("answer__votes"),
            num_answers=Count("answer"),
            num_points=Coalesce(Sum("answer__votes"), 0), # default to 0 if user has no  answers
        )
        
        if query_params:
            users = users.filter(search=query_params).order_by("-rank", "username")
        else:
            users = users.order_by("username")

        # Default 25 users per page for now
        paginator = Paginator(users, 24)

        page = request.GET.get("page")
        paginated_users = paginator.get_page(page)
        search_text = query_params if query_params != None else ""
        notification_list = notification_helper.get_notifications(request.user)
        context = {
            "user_list": paginated_users,
            "search_text": search_text,
            "notifications": notification_list,
        }

        return render(request, "exchange/users.html", context)
