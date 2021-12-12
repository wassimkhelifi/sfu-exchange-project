from django.core import paginator
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator 

from ..models import User 

def UsersView(request):
    users = User.objects.all()
    # Default 25 users per page for now
    paginator = Paginator(users, 25) 

    page = request.GET.get('page')
    paginated_users = paginator.get_page(page)
    return render(
        request, 'exchange/users.html', {
            'user_list': paginated_users
        }
    )