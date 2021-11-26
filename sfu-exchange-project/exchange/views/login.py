from django.shortcuts import render
from django.http import HttpResponse



def LoginView(request):
    return HttpResponse('<h1>Login Page</h1>')
