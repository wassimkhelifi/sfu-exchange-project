from django.shortcuts import render
from django.http import HttpResponse



def LoginView(request):
    return render(request, 'exchange/login.html')
