from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.urls import reverse

from ..models import Question, Tag, User
from ..forms import QuestionForm

def QuestionSubmitView(request):
  if request.method == 'POST':
    form = QuestionForm(request.POST)

    if form.is_valid():
      user = User.objects.latest('id')
      tags = form.cleaned_data.get('tags')
      createdQuestion = Question.objects.create(
        title=form.cleaned_data['title'], 
        question_text=form.cleaned_data['question_text'],
        user_id=user
      )
      createdQuestion.tags.set(tags)
      return HttpResponseRedirect('exchange/questions', kwargs={'question_id': createdQuestion.id})
  else:
    form = QuestionForm()

  context = {
    'form': form,
  }

  return render(request, 'exchange/questions_submit.html', context)