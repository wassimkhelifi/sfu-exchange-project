from django.shortcuts import render
from django.http import HttpResponse



def UsersView(request):
    return HttpResponse('<h1>Users Page</h1>')