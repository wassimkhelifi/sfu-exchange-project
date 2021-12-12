from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..forms import RegistrationForm
from django.contrib.auth import login
from django.contrib import messages
from ..models import Role


def RegisterView(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Add a default role here, as ManyToManyField does not allow default values
            student_role = Role.objects.filter(name='Student').first()
            user.roles.add(student_role)
            user.save()
            
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("Home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = RegistrationForm()
    return render (request=request, template_name="exchange/register.html", context={"form":form})
