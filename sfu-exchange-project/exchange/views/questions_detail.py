from django.shortcuts import render
from django.http import HttpResponse, Http404

from ..models import Question

def QuestionsDetailView(request, question_id,):
  try:
    question = Question.objects.get(pk=question_id)
  except Question.DoesNotExist:
    raise Http404('Question does not exist!')
    
  return render(request, 'exchange/questions_detail.html', {
    'question': question,
  })