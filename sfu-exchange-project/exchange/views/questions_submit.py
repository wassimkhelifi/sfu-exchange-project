from django.shortcuts import redirect, render, get_object_or_404
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from ..helpers import notification_helper

from ..models import Question, User
from ..forms import QuestionForm

@login_required(login_url='Login')
def QuestionSubmitView(request, id=None):
  
  if request.method == 'POST':
    if not request.user.is_authenticated:
      return HttpResponse('Unauthorized', status=401)

    if id:
        question = Question.objects.filter(id=id).first()
        form = QuestionForm(request.POST, instance=question)
    else:
        form = QuestionForm(request.POST)

    if form.is_valid():
      if id:
        form.save()
        return redirect('Questions_Detail', question_id=question.id, slug=question.slug)
      else:
        user = User.objects.get(username=request.user)
        tags = form.cleaned_data.get('tags')
        createdQuestion = Question.objects.create(
          title=form.cleaned_data['title'], 
          question_text=form.cleaned_data['question_text'],
          anonymous=form.cleaned_data['anonymous'],
          user_id=user
        )
        notification_helper.create_notification(
            request.user, 
            {
                'notification_title': createdQuestion.title,
                'notification_text': 'question created!',
                'notification_type': 'new question',
                'url': f"/exchange/questions/{createdQuestion.id}/{createdQuestion.slug}",
            }
        )
        createdQuestion.tags.set(tags)
        return redirect('Questions_Detail', question_id=createdQuestion.id, slug=createdQuestion.slug)
  else:
    if id:
      question = Question.objects.filter(id=id).first()
      form = QuestionForm(instance=question)
    else:
      form = QuestionForm()

  notification_list = notification_helper.get_notifications(request.user)
  context = {
    'form': form,
    'notifications': notification_list,
  }

  return render(request, 'exchange/questions_submit.html', context)