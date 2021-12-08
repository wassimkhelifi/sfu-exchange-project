from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    bio = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=100)

    class Meta:
        model = User
        fields = '__all__'

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        if commit:
            user.save()
        return user