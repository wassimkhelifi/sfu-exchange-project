from django.core import paginator
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Count, Sum, query
from django.db.models.functions import Coalesce
from django.db.models import Q
from ..models import User


def UsersView(request, page=""):
    if request.method == "GET":
        query_params = request.GET.get("q")
        # Conditionally query users, otherwise return all
        if query_params:
            users = User.objects.filter(
                Q(username__icontains=query_params)
                | Q(first_name__icontains=query_params)
                | Q(last_name__icontains=query_params)
                | Q(email__icontains=query_params)
            )
            print("@@@USERSVIEW: search query:", query_params)
        else:
            users = User.objects
        users = users.annotate(
            num_posts=Count("answer__votes"),
            num_answers=Count("answer"),
            num_points=Coalesce(
                Sum("answer__votes"), 0
            ),  # default to 0 if user has no  answers
        ).order_by('username')
        # Default 25 users per page for now
        paginator = Paginator(users, 24)

        page = request.GET.get("page")
        paginated_users = paginator.get_page(page)
        return render(request, "exchange/users.html", {"user_list": paginated_users, "search_text": query_params})
