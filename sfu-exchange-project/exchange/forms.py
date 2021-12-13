from django import forms
from django.forms import widgets
from .models import Faculty, User, Tag, Answer
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator


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


class QuestionForm(forms.Form):
    title = forms.CharField(max_length=150)
    # TODO: Max length of stackoverflow body is 30k characters, need to change model limit. : https://meta.stackexchange.com/questions/176445/knowing-your-limits-what-is-the-maximum-length-of-a-question-title-post-image
    question_text = forms.CharField(max_length=3000)
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple
    )
    user_id = 1
    anonymous = forms.BooleanField(required=False)

    # TODO: Potentially provide validation if needed, otherwise we can remove these functions
    def clean_title(self):
        data = self.cleaned_data["title"]
        return data

    def clean_questions_text(self):
        data = self.cleaned_data["question_text"]
        return data


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

