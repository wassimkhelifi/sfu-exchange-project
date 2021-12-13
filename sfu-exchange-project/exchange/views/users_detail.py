from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.http import Http404

from ..helpers import user_helper
from ..models import User
from ..forms import ProfileEditForm

def UsersDetailView(request, user_id, user_username):
  try:
    user = User.objects.get(pk=user_id)
  except User.DoesNotExist:
    raise Http404("User does not exist!")

  questions = user_helper.get_user_top_questions(user)
  tags = user_helper.get_user_top_tags(user)
  user_helper.format_user(user)

  paginator = Paginator(questions, 2)
  page = request.GET.get('page')
  paginated_questions = paginator.get_page(page)

  context = { 
      'userProfile': user or {},
      'questions': paginated_questions or {},
      'tags': tags or {}
  }

  return render(request, 'exchange/users_detail.html', context)