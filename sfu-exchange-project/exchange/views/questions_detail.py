from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import Http404

from ..models import Question, Answer, User
from ..forms import AnswerForm

def QuestionsDetailView(request, question_id,):
  try:
    current_question = Question.objects.get(pk=question_id)
    answerForm = AnswerForm()
    
  except Question.DoesNotExist:
    raise Http404('Question does not exist!')
  
  if request.method == 'POST':
    answerSubmission = AnswerForm(request.POST)

    if answerSubmission.is_valid():
      # TODO: Get a the latest user for now until we have user login completed to get the current user posting
      current_user = User.objects.latest('id')
      Answer.objects.create(
        answer_text = answerSubmission.cleaned_data['answer_text'],
        anonymous = answerSubmission.cleaned_data['anonymous'],
        user_id = current_user,
        question_id = current_question
      )

  answers = Answer.objects.filter(question_id=question_id)
  if not answers:
    answers = None

  return render(request, 'exchange/questions_detail.html', {
    'question': current_question,
    'answers': answers,
    'answerForm': answerForm
  })