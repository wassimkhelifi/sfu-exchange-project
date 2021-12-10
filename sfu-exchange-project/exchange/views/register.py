from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..forms import RegistrationForm
from django.contrib.auth import login
from django.contrib import messages


def RegisterView(request):
    print("got to register view")
    if request.method == "POST":
        print('@@@@@@@@@@@@ INSIDE POST @@@@@@@@@@@@')
        form = RegistrationForm(request.POST)
        print('@@POST: form', form)
        if form.is_valid():
            user = form.save()
            #login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("Home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        print("@@@@@@@@@@@@ NOT INSIDE POST @@@@@@@@@@@@")
        form = RegistrationForm()
    return render (request=request, template_name="exchange/register.html", context={"form":form})
    # return render(request, 'exchange/register.html')
