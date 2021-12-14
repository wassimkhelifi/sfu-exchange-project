from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from ..helpers import user_helper, notification_helper
from ..models import User
from ..forms import ProfileEditForm

# def UsersDetailView(request, user_id, user_username):
#   try:
#     user = User.objects.get(pk=user_id)
#   except User.DoesNotExist:
#     raise Http404("User does not exist!")

#   questions = user_helper.get_user_top_questions(user)
#   user_helper.format_user(user)

#   paginator = Paginator(questions, 2)
#   page = request.GET.get('page')
#   paginated_questions = paginator.get_page(page)

#   context = { 
#       'userProfile': user or {},
#       'questions': paginated_questions or {},
#   }

#   return render(request, 'exchange/users_detail.html', context)

def UsersDetailView(request, user_id='', user_username=''):
    try:
      user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
      raise Http404("User does not exist!")

    questions = user_helper.get_user_top_questions(user)
    user_helper.format_user(user)
    notification_list = notification_helper.get_notifications(request.user)

    paginator = Paginator(questions, 2)
    page = request.GET.get('page')
    paginated_questions = paginator.get_page(page)

    context = { 
        'userProfile': user or {},
        'can_edit': user == request.user,
        'notifications': notification_list or {},
        'questions': paginated_questions or {},
    }

    return render(request, 'exchange/users_detail.html', context)