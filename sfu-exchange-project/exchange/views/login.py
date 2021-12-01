from django.shortcuts import render



def LoginView(request):
    return render(request, 'exchange/login.html')
