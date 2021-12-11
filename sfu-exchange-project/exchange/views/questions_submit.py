from django.shortcuts import redirect, render

from ..models import Question, User
from ..forms import QuestionForm

def QuestionSubmitView(request):
  if request.method == 'POST':
    form = QuestionForm(request.POST)

    if form.is_valid():
      # TODO: Get the latest user for now until we have user login completed to get the current user posting
      user = User.objects.latest('id')
      tags = form.cleaned_data.get('tags')
      createdQuestion = Question.objects.create(
        title=form.cleaned_data['title'], 
        question_text=form.cleaned_data['question_text'],
        user_id=user
      )
      createdQuestion.tags.set(tags)
      return redirect('Questions_Detail', question_id=createdQuestion.id)
  else:
    form = QuestionForm()

  context = {
    'form': form,
  }

  return render(request, 'exchange/questions_submit.html', context)