from django.core import paginator
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce

from ..models import User


def UsersView(request):
    users = User.objects.annotate(
        num_posts=Count("answer__votes"),
        num_answers=Count("answer"),
        num_points=Coalesce(Sum("answer__votes"),0), # default to 0 if user has no  answers
    )
    # Default 25 users per page for now
    paginator = Paginator(users, 24)

    page = request.GET.get("page")
    paginated_users = paginator.get_page(page)
    return render(request, "exchange/users.html", {"user_list": paginated_users})
