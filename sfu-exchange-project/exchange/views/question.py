from django.shortcuts import render
from django.http import HttpResponse



def QuestionView(request):
    return HttpResponse('<h1>Question Page</h1>')
