from django.shortcuts import render
from django.http import HttpResponse



def TagsView(request):
    return HttpResponse('<h1>Tags Page</h1>')