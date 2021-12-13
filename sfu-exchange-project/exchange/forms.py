from django import forms
from django.forms import widgets
from .models import Faculty, Question, User, Tag, Answer
from django.contrib.auth.forms import UserCreationForm
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


IMG_CHOICES = (
    ("racoon.png", "Racoon"),
    ("moose.png", "Moose"),
    ("beaver.png", "Beaver"),
    ("orca.png", "Orca"),
    ("bear.png", "Bear"),
)



class RegistrationForm(UserCreationForm):
    # Fields we redefine here overwrite those in the form. By default, they are 'required'
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=100)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
            "faculty_id",
            "bio",
            "img"
        ]
        widgets = {
            "img": forms.Select(choices=IMG_CHOICES, attrs={"class": "form-control"}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            "title",
            "question_text",
            "tags",
            "anonymous"
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder":"Post Title"}),
            "question_text": SummernoteWidget(),
        }



class AnswerForm(forms.Form):
    answer_text = forms.CharField(max_length=3000)
    anonymous = forms.BooleanField(required=False)


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "bio",
            "img",
            "faculty_id"
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder":"First Name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter a short bio..."}),
            "img": forms.Select(choices=IMG_CHOICES, attrs={"class": "form-control"}),
            "faculty_id": forms.Select(attrs={"class": "form-control"}),
        }

