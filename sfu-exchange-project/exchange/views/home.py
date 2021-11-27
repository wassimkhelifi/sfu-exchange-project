from django.shortcuts import render
from django.http import HttpResponse



def HomeView(request):
    return HttpResponse('<h1>Home Page</h1>')
