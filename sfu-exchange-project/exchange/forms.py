from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    # Fields we redefine here overwrite those in the form. By default, they are 'required'
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=100)

    class Meta:
        model = User

        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'faculty_id', 'bio']
