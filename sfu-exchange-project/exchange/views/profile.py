from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..helpers import user_helper
from ..models import User


@login_required
def ProfileView(request):
    user = User.objects.get(pk=request.user.id)
    questions = user_helper.get_user_top_questions(user)
    tags = user_helper.get_user_top_tags(user)
    user_helper.format_user(user)

    context = { 
        'user': user or {},
        'questions': questions or {},
        'tags': tags or {}
    }
    return render(request, 'exchange/profile.html', context)


def ProfileEditView(request):
    return render(request, 'exchange/profileEdit.html')
