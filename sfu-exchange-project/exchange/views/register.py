from django.shortcuts import render
from django.http import HttpResponse



def RegisterView(request):
    return render(request, 'exchange/register.html')
