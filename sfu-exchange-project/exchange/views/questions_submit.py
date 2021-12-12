from django.shortcuts import redirect, render
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required

from ..models import Question, User
from ..forms import QuestionForm

@login_required(login_url='Login')
def QuestionSubmitView(request):
  if request.method == 'POST':
    if not request.user.is_authenticated:
      return HttpResponse('Unauthorized', status=401)

    form = QuestionForm(request.POST)

    if form.is_valid():
      user = User.objects.get(username=request.user)
      tags = form.cleaned_data.get('tags')
      createdQuestion = Question.objects.create(
        title=form.cleaned_data['title'], 
        question_text=form.cleaned_data['question_text'],
        anonymous=form.cleaned_data['anonymous'],
        user_id=user
      )
      createdQuestion.tags.set(tags)
      return redirect('Questions_Detail', question_id=createdQuestion.id, slug=createdQuestion.slug)
  else:
    form = QuestionForm()

  context = {
    'form': form,
  }

  return render(request, 'exchange/questions_submit.html', context)