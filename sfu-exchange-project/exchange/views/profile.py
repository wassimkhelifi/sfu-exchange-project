from django.shortcuts import render
from django.http import HttpResponse



def ProfileView(request):
    return HttpResponse('<h1>Profile Page</h1>')

def ProfileEditView(request):
    return HttpResponse('<h1>Profile Edit Page</h1>')
