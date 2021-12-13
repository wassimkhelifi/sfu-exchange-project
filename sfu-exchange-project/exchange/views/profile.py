from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from ..helpers import user_helper, notification_helper
from ..models import User
from ..forms import ProfileEditForm

@login_required
def ProfileView(request):
    user = User.objects.get(pk=request.user.id)
    questions = user_helper.get_user_top_questions(user)
    tags = user_helper.get_user_top_tags(user)
    user_helper.format_user(user)
    notification_list = notification_helper.get_notifications(request.user)

    context = { 
        'user': user or {},
        'questions': questions or {},
        'tags': tags or {},
        'notifications': notification_list or {},
    }
    return render(request, 'exchange/profile.html', context)

@login_required
def ProfileEditView(request):
    instance = get_object_or_404(User, username=request.user)
    if request.method == "POST":
        form = ProfileEditForm(request.POST or None, instance=instance)
        if form.is_valid(): 
            # process form data
            
            form.save() 
            
            return HttpResponseRedirect("/exchange/profile/")
    else:
        user = request.user 
        form = ProfileEditForm(initial={
            "first_name": user.first_name,
            "last_name": user.last_name,
            "bio": user.bio,
            "img": user.img,
            "faculty_id": user.faculty_id
        })        
    notification_list = notification_helper.get_notifications(request.user)

    return render(request, 'exchange/profileEdit.html', {'form': form, 'notifications': notification_list})
