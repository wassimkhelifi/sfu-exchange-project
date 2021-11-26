from django.shortcuts import render
from django.http import HttpResponse

def QuestionsDetailView(request):
  return HttpResponse('<h1>Question Detail Page</h1>')