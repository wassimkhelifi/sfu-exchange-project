from django import forms
from .models import User, Tag, Answer, Question
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404

class RegistrationForm(UserCreationForm):
    # Fields we redefine here overwrite those in the form. By default, they are 'required'
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=100)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'faculty_id', 'bio']

class QuestionForm(forms.Form):
    title = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'title-field'}))
    # TODO: Max length of stackoverflow body is 30k characters, need to change model limit. : https://meta.stackexchange.com/questions/176445/knowing-your-limits-what-is-the-maximum-length-of-a-question-title-post-image
    question_text = forms.CharField(widget=forms.Textarea(attrs={'class': 'body-field'}))
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': 'tags-field'}))
    user_id = 1
    anonymous = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'anonymous-field'}))
    
    # TODO: Potentially provide validation if needed, otherwise we can remove these functions
    def clean_title(self):
        data = self.cleaned_data['title']
        return data

    def clean_questions_text(self):
        data = self.cleaned_data['question_text']
        return data

    class Meta:
        model = Question


class AnswerForm(forms.Form):
    answer_text = forms.CharField(widget=forms.Textarea(attrs={'class': 'answer-field'}))
    anonymous = forms.BooleanField(required=False)

    class Meta:
        model = Answer
