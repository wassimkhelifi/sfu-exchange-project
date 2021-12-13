from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from ..helpers import user_helper
from ..models import User


@login_required
def ProfileView(request):
    user = User.objects.get(pk=request.user.id)
    questions = user_helper.get_user_top_questions(user)
    tags = user_helper.get_user_top_tags(user)
    user_helper.format_user(user)

    paginator = Paginator(questions, 2)
    page = request.GET.get('page')
    paginated_questions = paginator.get_page(page)

    context = { 
        'user': user or {},
        'questions': paginated_questions or {},
        'tags': tags or {}
    }
    return render(request, 'exchange/profile.html', context)


def ProfileEditView(request):
    return render(request, 'exchange/profileEdit.html')
