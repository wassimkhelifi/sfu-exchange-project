import random

from django.shortcuts import render
from ..helpers import user_helper
from ..models import User, Question



def ProfileView(request):
    # choose a question, get its user, use that user for the demo; TODO: remove
    q_pks = Question.objects.values_list('pk', flat=True)
    q_pk = random.choice(q_pks)
    q = Question.objects.get(pk=q_pk)

    user = User.objects.get(pk=q.user_id.id)
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
